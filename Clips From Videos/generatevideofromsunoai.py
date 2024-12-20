import os
import requests
import shutil
import json
import re
import time

from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pydub import AudioSegment
import nltk
import spacy

# Ensure NLTK data is downloaded
nltk.download('punkt')

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm' model for spaCy...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Configuration
SUNO_API_KEY = 'c49551361ab34d3d8a282ff5d3c6d802'  # Replace with your Suno AI API Key
PIXABAY_API_KEY = '47743649-5733ba1681a60793a017da96b'  # Replace with your Pixabay API Key
OUTPUT_VIDEO = 'final_video.mp4'
TEMP_VIDEO_DIR = 'temp_videos'
TEMP_AUDIO = 'temp_audio.mp3'
GENERATED_AUDIO = 'generated_audio.mp3'

def generate_mp3_from_prompt(prompt, output_path, max_retries=3, backoff_factor=2):
    """
    Generates an MP3 file from the given prompt using Suno AI API with retry logic.
    """
    url = 'https://api.suno.ai/v1/audio/generate'  # Update to the correct Suno AI API endpoint

    headers = {
        'Authorization': f'Bearer {SUNO_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'prompt': prompt,
        'voice': 'default',  # Adjust parameters as per Suno AI's API
        'format': 'mp3'
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, headers=headers, json=data, stream=True)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                print(f"Generated audio saved to {output_path}")
                return True
            elif response.status_code == 503:
                print(f"Service unavailable (503). Attempt {attempt} of {max_retries}. Retrying in {backoff_factor ** attempt} seconds...")
                time.sleep(backoff_factor ** attempt)
            elif response.status_code == 401:
                print("Unauthorized. Check your API key.")
                return False
            else:
                print(f"Failed to generate audio. Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return False

    print("Max retries exceeded. Audio generation failed.")
    return False

def extract_tags_from_prompt(prompt, max_tags=5):
    """
    Extracts relevant tags from the prompt using NLP techniques.
    """
    doc = nlp(prompt.lower())
    # Extract nouns and proper nouns as potential tags
    tags = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]

    # Remove duplicates and common stopwords
    tags = list(set(tags))

    # Optionally, filter out less relevant words
    filtered_tags = [tag for tag in tags if len(tag) > 2]  # Simple filter; adjust as needed

    # Limit the number of tags
    return filtered_tags[:max_tags]

def search_and_download_videos(api_key, tags, videos_per_tag, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    base_url = 'https://pixabay.com/api/videos/'
    all_video_urls = []

    for tag in tags:
        params = {
            'key': api_key,
            'q': tag,
            'per_page': videos_per_tag,
            'safesearch': 'true'
        }
        try:
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                print(f"Failed to fetch videos for tag '{tag}'. Status Code: {response.status_code}")
                continue
            data = response.json()
            for hit in data.get('hits', []):
                # Select the video with the highest resolution available
                videos = hit.get('videos', {})
                if 'large' in videos:
                    video_url = videos['large']['url']
                elif 'medium' in videos:
                    video_url = videos['medium']['url']
                elif 'small' in videos:
                    video_url = videos['small']['url']
                else:
                    continue  # Skip if no suitable video size found
                all_video_urls.append(video_url)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching videos for tag '{tag}': {e}")

    print(f"Found {len(all_video_urls)} videos. Starting download...")
    for idx, url in enumerate(all_video_urls, start=1):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                video_path = os.path.join(download_path, f'video_{idx}.mp4')
                with open(video_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                print(f"Downloaded: {video_path}")
            else:
                print(f"Failed to download video from {url}. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video from {url}: {e}")

def merge_videos(video_dir, output_path):
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    video_clips = []
    for vf in video_files:
        try:
            clip = VideoFileClip(vf)
            video_clips.append(clip)
        except Exception as e:
            print(f"Error loading video file {vf}: {e}")

    if not video_clips:
        print("No videos to merge.")
        return None

    try:
        final_clip = concatenate_videoclips(video_clips, method='compose')
        final_clip.write_videofile(output_path, codec='libx264', audio=False)
        final_clip.close()
        print(f"Merged video saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error merging videos: {e}")
        return None

def modify_audio(input_audio_path, output_audio_path, target_length):
    """
    Modify the audio to match the target length by adjusting speed.
    This is a simple method and may affect audio quality.
    """
    try:
        audio = AudioSegment.from_mp3(input_audio_path)
        original_length = len(audio)
        speed_change = original_length / target_length
        # Limit speed change to avoid extreme alterations
        speed_change = max(0.5, min(speed_change, 2.0))
        # Adjust speed
        modified_audio = audio.speedup(playback_speed=speed_change)
        modified_audio.export(output_audio_path, format="mp3")
        print(f"Modified audio saved to {output_audio_path}")
    except Exception as e:
        print(f"Error modifying audio: {e}")

def add_audio_to_video(video_path, audio_path, output_path):
    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Set audio to video
        final_video = video.set_audio(audio)
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

        # Close clips
        video.close()
        audio.close()
        final_video.close()
        print(f"Final video with audio saved to {output_path}")
    except Exception as e:
        print(f"Error adding audio to video: {e}")

def main():
    # Step 0: Get user prompt
    prompt = input("Enter your prompt for Suno AI to generate MP3: ").strip()
    if not prompt:
        print("No prompt provided. Exiting.")
        return

    # Step 1: Generate MP3 from prompt using Suno AI
    success = generate_mp3_from_prompt(prompt, GENERATED_AUDIO)
    if not success:
        print("Audio generation failed. Exiting.")
        return

    # Step 2: Extract tags from prompt
    tags = extract_tags_from_prompt(prompt)
    if not tags:
        print("No tags extracted from prompt. Exiting.")
        return
    print(f"Extracted Tags: {tags}")

    # Step 3: Search and download videos from Pixabay
    VIDEOS_PER_TAG = 3  # Adjust as needed
    search_and_download_videos(PIXABAY_API_KEY, tags, VIDEOS_PER_TAG, TEMP_VIDEO_DIR)

    # Step 4: Merge downloaded videos
    merged_video_path = 'merged_video.mp4'
    merge_videos(TEMP_VIDEO_DIR, merged_video_path)

    if not os.path.exists(merged_video_path):
        print("Merged video not found. Exiting.")
        return

    # Step 5: Modify audio to match video length
    try:
        video_clip = VideoFileClip(merged_video_path)
        video_duration = video_clip.duration  # in seconds
        video_clip.close()
    except Exception as e:
        print(f"Error loading merged video: {e}")
        return

    # Convert video_duration to milliseconds for pydub
    target_length_ms = int(video_duration * 1000)

    modify_audio(GENERATED_AUDIO, TEMP_AUDIO, target_length_ms)

    if not os.path.exists(TEMP_AUDIO):
        print("Modified audio not found. Exiting.")
        return

    # Step 6: Merge audio with video
    add_audio_to_video(merged_video_path, TEMP_AUDIO, OUTPUT_VIDEO)

    # Cleanup temporary files
    shutil.rmtree(TEMP_VIDEO_DIR, ignore_errors=True)
    if os.path.exists(TEMP_AUDIO):
        os.remove(TEMP_AUDIO)
    if os.path.exists(merged_video_path):
        os.remove(merged_video_path)
    if os.path.exists(GENERATED_AUDIO):
        os.remove(GENERATED_AUDIO)

    print("Process completed successfully. Check the 'final_video.mp4' file.")

if __name__ == "__main__":
    main()
