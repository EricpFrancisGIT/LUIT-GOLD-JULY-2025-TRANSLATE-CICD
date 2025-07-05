import os
import boto3
import json
import time
from pathlib import Path

AWS_REGION = os.environ['AWS_REGION']
S3_BUCKET = os.environ['S3_BUCKET']
S3_PREFIX = os.environ.get('S3_PREFIX', 'BETA/')
DESTINATION_LANG = os.environ.get('DESTINATION_LANG', 'cy')

s3 = boto3.client('s3', region_name=AWS_REGION)
transcribe = boto3.client('transcribe', region_name=AWS_REGION)
translate = boto3.client('translate', region_name=AWS_REGION)
polly = boto3.client('polly', region_name=AWS_REGION)

def upload_to_s3(local_path, s3_key):
    s3.upload_file(local_path, S3_BUCKET, s3_key)

def transcribe_audio(file):
    job_name = f'job-{int(time.time())}'
    s3_url = f's3://{S3_BUCKET}/{S3_PREFIX}audio_inputs/{file}'

    transcript_s3_key = f'{S3_PREFIX}transcripts/{job_name}.json'

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_url},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=S3_BUCKET,
        OutputKey=transcript_s3_key
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(5)

    return transcript_s3_key

def translate_text(text, target_lang):
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=DESTINATION_LANG)
    return result['TranslatedText']

def synthesize_speech(text, lang_code, output_path):
    voice_map = {
        'de': 'Vicki',
        'en': 'Joanna',
        'fr': 'Celine',
        'es': 'Penelope'
    }

    voice_id = voice_map.get(lang_code, 'Joanna')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id
    )
    with open(output_path, 'wb') as f:
        f.write(response['AudioStream'].read())

def process_file(filepath):
    filename = Path(filepath).name
    s3_key = f'{S3_PREFIX}audio_inputs/{filename}'
    s3.upload_file(filepath, S3_BUCKET, s3_key)
    print(f'Uploaded {filename} to S3 at {s3_key}')

    transcript_s3_key = transcribe_audio(filename)

    local_transcript_json = "/tmp/tmp_transcript.json"
    s3.download_file(S3_BUCKET, transcript_s3_key, local_transcript_json)

    try:
        with open(local_transcript_json) as f:
            json_data = json.load(f)
        transcript_text = json_data['results']['transcripts'][0]['transcript']
    except Exception as e:
        raise Exception("Error reading transcript JSON file. Please try again") from e
    
    translated_text = translate_text(transcript_text, DESTINATION_LANG)

    transcript_path = f"/tmp/{filename}_transcript.txt"
    translated_path = f"/tmp/{filename}__{DESTINATION_LANG}.txt"
    output_audio_path = f"audio_outputs/{filename}_{DESTINATION_LANG}.mp3"

    with open("tmp_transcript.txt", "w") as f:
        f.write(transcript_text)
    with open("tmp_translated.txt", "w") as f:
        f.write(translated_text)
    
    synthesize_speech(translated_text, DESTINATION_LANG, "tmp_audio.mp3")

    upload_to_s3("tmp_transcript.txt", f"{S3_PREFIX}{transcript_path}")
    upload_to_s3("tmp_translated.txt", f"{S3_PREFIX}{translated_path}")
    upload_to_s3("tmp_audio.mp3", f"{S3_PREFIX}{output_audio_path}")

for file in Path("audio_inputs").glob("*.mp3"):
    process_file(file)
    print(f'Processed {file.name}')
