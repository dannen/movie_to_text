import os
import subprocess
import sys
from google.cloud import storage, speech
from google.api_core.exceptions import RetryError, DeadlineExceeded
import time

# Hardcoded Google Cloud credentials and bucket name
credentials_path = "/path/to/your/service_account_json_key.json"
bucket_name = "your_bucket_name"

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Initialize Google Cloud clients
storage_client = storage.Client()
speech_client = speech.SpeechClient()

def download_video(url, output_path):
    if not os.path.exists(output_path):
        print(f"Downloading video from {url}")
        subprocess.run(["wget", url, "-O", output_path])
    else:
        print(f"Video file {output_path} already exists. Skipping download.")

def extract_audio(video_path, audio_path):
    # Overwrite the audio file if it exists
    if os.path.exists(audio_path):
        os.remove(audio_path)
    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path])

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def transcribe_audio(bucket_name, audio_file_path, transcript_file_path):
    gcs_uri = f"gs://{bucket_name}/{audio_file_path}"
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=44100,
        language_code="en-US",
    )
    
    # Increase the timeout period
    timeout = 600  # 10 minutes
    try:
        operation = speech_client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=timeout)

        with open(transcript_file_path, "w") as f:
            for result in response.results:
                f.write(result.alternatives[0].transcript + "\n")

    except (RetryError, DeadlineExceeded) as e:
        print(f"Transcription operation timed out: {e}")
        # Retry mechanism
        time.sleep(10)  # Wait for 10 seconds before retrying
        return transcribe_audio(bucket_name, audio_file_path, transcript_file_path)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 movie_to_text.py target.mp4")
        sys.exit(1)

    video_file_path = sys.argv[1]
    if not os.path.exists(video_file_path):
        print(f"Video file {video_file_path} does not exist.")
        sys.exit(1)
    
    audio_file_path = video_file_path.replace(".mp4", ".mp3")
    transcript_file_path = video_file_path.replace(".mp4", ".txt")

    # Extract audio from the video
    extract_audio(video_file_path, audio_file_path)

    # Upload audio to Cloud Storage
    upload_to_bucket(bucket_name, audio_file_path, os.path.basename(audio_file_path))

    # Transcribe the audio
    transcribe_audio(bucket_name, os.path.basename(audio_file_path), transcript_file_path)

if __name__ == "__main__":
    main()
