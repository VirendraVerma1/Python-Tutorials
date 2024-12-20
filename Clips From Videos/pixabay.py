import os
import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pydub import AudioSegment
import shutil

# Configuration
PIXABAY_API_KEY = '47743649-5733ba1681a60793a017da96b'  # Replace with your Pixabay API Key
TAGS = ['nature', 'sunrise']  # Replace with your desired tags
VIDEOS_PER_TAG = 3  # Number of videos to download per tag
OUTPUT_VIDEO = 'final_video.mp4'
INPUT_AUDIO = 'murli.mp3'  # Path to your MP3 file
TEMP_VIDEO_DIR = 'temp_videos'
TEMP_AUDIO = 'temp_audio.mp3'

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
                print(f"Failed to download video from {url}")
        except Exception as e:
            print(f"Error downloading video from {url}: {e}")

def modify_audio(input_audio_path, output_audio_path, target_length):
    """
    Modify the audio to match the target length by adjusting speed.
    This is a simple method and may affect audio quality.
    """
    try:
        audio = AudioSegment.from_mp3(input_audio_path)
        original_length = len(audio)
        speed_change = original_length / target_length
        # Adjust speed
        modified_audio = audio.speedup(playback_speed=speed_change)
        modified_audio.export(output_audio_path, format="mp3")
        print(f"Modified audio saved to {output_audio_path}")
    except Exception as e:
        print(f"Error modifying audio: {e}")

def merge_videos(video_dir, output_path):
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    video_clips = []
    for vf in video_files:
        clip = VideoFileClip(vf)
        video_clips.append(clip)
    
    if not video_clips:
        print("No videos to merge.")
        return None
    
    final_clip = concatenate_videoclips(video_clips, method='compose')
    final_clip.write_videofile(output_path, codec='libx264', audio=False)
    final_clip.close()
    print(f"Merged video saved to {output_path}")
    return output_path

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
    # Step 1: Search and download videos
    search_and_download_videos(PIXABAY_API_KEY, TAGS, VIDEOS_PER_TAG, TEMP_VIDEO_DIR)
    
    # Step 2: Merge videos
    merged_video_path = 'merged_video.mp4'
    merge_videos(TEMP_VIDEO_DIR, merged_video_path)
    
    if not os.path.exists(merged_video_path):
        print("Merged video not found. Exiting.")
        return
    
    # Step 3: Modify audio to match video length
    video_clip = VideoFileClip(merged_video_path)
    video_duration = video_clip.duration  # in seconds
    video_clip.close()
    
    # Convert video_duration to milliseconds for pydub
    target_length_ms = int(video_duration * 1000)
    
    modify_audio(INPUT_AUDIO, TEMP_AUDIO, target_length_ms)
    
    if not os.path.exists(TEMP_AUDIO):
        print("Modified audio not found. Exiting.")
        return
    
    # Step 4: Merge audio with video
    add_audio_to_video(merged_video_path, TEMP_AUDIO, OUTPUT_VIDEO)
    
    # Cleanup temporary files
    shutil.rmtree(TEMP_VIDEO_DIR, ignore_errors=True)
    if os.path.exists(TEMP_AUDIO):
        os.remove(TEMP_AUDIO)
    if os.path.exists(merged_video_path):
        os.remove(merged_video_path)
    
    print("Process completed successfully.")

if __name__ == "__main__":
    main()
