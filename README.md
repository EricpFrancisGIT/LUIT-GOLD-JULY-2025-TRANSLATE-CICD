# 🎙️ Multilingual Audio Transformation Pipeline

> Automate audio transcription, translation, and regeneration using AWS AI Services and GitHub Actions.

## 📚 Project Overview

Pixel Learning Co., a digital-first education startup, is committed to accessibility and language inclusion. This pipeline enables the automated conversion of instructor-recorded `.mp3` messages into multiple languages using Amazon Transcribe, Translate, Polly, and S3. It is fully orchestrated using GitHub Actions and requires no manual processing once integrated into the team's content workflow.

---

## 🎯 Objectives

- **Transcribe** `.mp3` audio content to English text using Amazon Transcribe  
- **Translate** the text into target languages (e.g., Spanish, French) using Amazon Translate  
- **Synthesize** the translated text into speech using Amazon Polly  
- **Store** all outputs in an organized folder structure in an S3 bucket (separated by beta/prod)  
- **Automate** everything using GitHub Actions with separate workflows for pull requests and merges  

---

## 🛠️ Requirements

### AWS Services Used
- Amazon S3 (for storing inputs/outputs)
- Amazon Transcribe
- Amazon Translate
- Amazon Polly

### GitHub Actions
- Pull Request Workflow → Deploys to `beta/`
- Merge Workflow → Deploys to `prod/`

---

## 🧱 Project Structure

├── audio_inputs/ # Add .mp3 files here for processing
├── .github/
│ └── workflows/
│ ├── on_pull_request.yml
│ └── on_merge.yml
├── process_audio.py # Main processing script
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions

### 1. 🧰 AWS Configuration

Before using the pipeline, ensure the following:

- An S3 bucket is created (e.g., `pixel-audio-pipeline`)
- IAM User or Role has the following permissions:
  - `transcribe:StartTranscriptionJob`, `transcribe:GetTranscriptionJob`
  - `translate:TranslateText`
  - `polly:SynthesizeSpeech`
  - `s3:PutObject`, `s3:GetObject`

### 2. 🔐 GitHub Secrets Setup

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**  
Add the following secrets:

| Name               | Description                          |
|--------------------|--------------------------------------|
| `AWS_ACCESS_KEY_ID`     | Your AWS access key              |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret access key       |
| `AWS_REGION`            | AWS region (e.g., `us-east-1`)   |
| `S3_BUCKET`             | Name of your S3 bucket           |
| `TARGET_LANG`           | Language code (e.g., `es`, `fr`) |

### 3. 📦 Install Dependencies (Optional for local testing)

```bash
pip install -r requirements.txt

🚀 Usage
Step 1: Upload Audio File
Add .mp3 files to the audio_inputs/ folder and push to a feature branch.

Step 2: Trigger Workflow
Create a Pull Request → triggers on_pull_request.yml, deploys to beta/

Merge into main → triggers on_merge.yml, deploys to prod/

Step 3: Check Outputs in S3
S3 output structure:

arduino
Copy
Edit
s3://your-bucket/
├── beta/
│   ├── transcripts/
│   ├── translations/
│   └── audio_outputs/
└── prod/
    ├── transcripts/
    ├── translations/
    └── audio_outputs/
Example paths:

beta/transcripts/sample.txt

prod/translations/sample_fr.txt

prod/audio_outputs/sample_fr.mp3

📜 Workflows Explained
.github/workflows/on_pull_request.yml
Trigger: Pull request to main

Runs process_audio.py

Uploads all artifacts to beta/ S3 prefix

.github/workflows/on_merge.yml
Trigger: Push to main (after merge)

Runs process_audio.py

Uploads all artifacts to prod/ S3 prefix

🧪 Example
Add instructor_message.mp3 to audio_inputs/

Create a PR

GitHub Action runs and processes:

Transcript → beta/transcripts/instructor_message.txt

Translation → beta/translations/instructor_message_es.txt

Audio → beta/audio_outputs/instructor_message_es.mp3

📄 License
This project is licensed under the MIT License.

🙌 Acknowledgments
Built with ❤️ using:

Amazon Transcribe

Amazon Translate

Amazon Polly

GitHub Actions
