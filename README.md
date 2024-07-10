
# Movie to Text

`movie_to_text.py` is a Python script that extracts audio from an MP4 video file, uploads the audio to Google Cloud Storage, and transcribes the audio to text using Google Cloud Speech-to-Text.

## Prerequisites

Before you begin, ensure you have the following:

1. A Google Cloud Platform account.
2. A project created in Google Cloud Platform.
3. Billing enabled for your Google Cloud project.
4. Google Cloud SDK installed on your local machine.
5. A service account with the necessary permissions and a JSON key file.

## Setup

### Step 1: Install Required Libraries

Install the required Python libraries:
```bash
pip install google-cloud-storage google-cloud-speech ffmpeg-python
```

### Step 2: Create and Configure a Google Cloud Project

1. **Create a new project** in the [Google Cloud Console](https://console.cloud.google.com/).
2. **Enable APIs**:
   - Enable the Cloud Speech-to-Text API.
   - Enable the Cloud Storage API.

3. **Create a Service Account**:
   - Go to "IAM & Admin" > "Service Accounts".
   - Create a new service account with the "Owner" role.
   - Generate a JSON key file for the service account and download it.

### Step 3: Upload the Service Account Key

1. **Upload the JSON key file** to your environment where you will run the script.
2. **Set the path** to the JSON key file in the `credentials_path` variable in the script.

### Step 4: Create a Cloud Storage Bucket

1. **Create a new bucket** in the [Google Cloud Storage](https://console.cloud.google.com/storage) section.
2. **Name your bucket** and choose your storage class and location settings.
3. **Set the `bucket_name`** variable in the script to the name of your bucket.

### Step 5: Update the Script

1. **Set the `credentials_path`** variable to the path of your service account JSON key file.
2. **Set the `bucket_name`** variable to the name of your Cloud Storage bucket.

### Step 6: Run the Script

Run the script with the path to your MP4 file as an argument:
```bash
python3 movie_to_text.py /path/to/your/target.mp4
```

## Script Explanation

- **Extract Audio**: Uses FFmpeg to extract audio from the MP4 file.
- **Upload to Google Cloud Storage**: Uploads the extracted audio file to a specified Google Cloud Storage bucket.
- **Transcribe Audio**: Uses Google Cloud Speech-to-Text to transcribe the audio file and save the transcript as a text file.

## Example Usage

To transcribe an MP4 file located at `/path/to/your/video.mp4`:
```bash
python3 movie_to_text.py /path/to/your/video.mp4
```

This will create an MP3 file and a TXT file in the same directory as the video file, with the audio extracted from the video and the transcript of the audio, respectively.

## Notes

- Ensure that FFmpeg is installed on your system and accessible from the command line.
- The script currently assumes that the video file exists locally. If you need to download it, you can uncomment and modify the `download_video` function as necessary.
