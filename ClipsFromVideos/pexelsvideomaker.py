import os
import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import shutil
import concurrent.futures
from moviepy.config import change_settings

# Optional: Specify FFmpeg binary if not in PATH
# change_settings({"FFMPEG_BINARY": "/path/to/ffmpeg"})

# Configuration
PEXELS_API_KEY = '1nL9vAaAjFa7HCGsJfDL3HIPAkRyDHJFkLLGv7T4QBhaYr0vRdaBrl29'  # Replace with your Pexels API Key
VIDEOS_PER_TAG = 20  # Number of videos to download per tag
MP3_FILES_DIR = 'mp3files'  # Directory containing MP3 files
OUTPUT_VIDEO_DIR = 'output_video'  # Directory to save the final videos
TEMP_VIDEO_DIR = 'temp_videos'  # Temporary directory for downloaded videos
MERGED_VIDEO_TEMPLATE = 'merged_video_{}.mp4'  # Template for merged video filenames
FINAL_OUTPUT_TEMPLATE = 'final_video_{}.mp4'  # Template for final output video filenames

# FFmpeg codec settings for GPU acceleration
FFMPEG_CODEC = 'h264_nvenc'  # NVIDIA NVENC H.264 encoder
FFMPEG_CODEC_PARAMS = {
    'codec': 'h264_nvenc',
    'preset': 'fast',       # Preset can be 'default', 'slow', 'medium', 'fast', etc.
    'bitrate': '5M',        # Adjust bitrate as needed (e.g., '5M' for 5 Mbps)
    'threads': '0',         # Let FFmpeg decide the number of threads
    # 'preset_flags': 'low_delay',  # Removed to fix TypeError
}

def search_and_download_videos(api_key, tag, videos_per_tag, download_path):
    """
    Searches for videos on Pexels based on a single tag and downloads them.

    :param api_key: Pexels API key.
    :param tag: Tag to search for.
    :param videos_per_tag: Number of videos to download.
    :param download_path: Directory to save downloaded videos.
    """
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    base_url = 'https://api.pexels.com/videos/search'
    all_video_urls = []

    headers = {
        'Authorization': api_key
    }

    per_page = min(videos_per_tag, 80)  # Pexels allows up to 80 per_page
    total_pages = (videos_per_tag // per_page) + (1 if videos_per_tag % per_page else 0)

    print(f"Fetching videos for tag: '{tag}'")

    for page in range(1, total_pages + 1):
        params = {
            'query': tag,
            'per_page': per_page,
            'page': page
        }
        print(f"Requesting page {page} for tag '{tag}'")
        response = requests.get(base_url, headers=headers, params=params)
        print(f"Request URL: {response.url}")
        if response.status_code != 200:
            print(f"Failed to fetch videos for tag '{tag}'. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return

        data = response.json()
        if 'videos' not in data:
            print(f"No 'videos' found in the response for tag '{tag}'. Response: {data}")
            return

        for video in data.get('videos', []):
            video_files = video.get('video_files', [])
            if not video_files:
                print(f"No video files found for video ID {video.get('id')}")
                continue

            # Select the video file with the highest resolution
            sorted_files = sorted(video_files, key=lambda x: x.get('width', 0), reverse=True)
            best_video = sorted_files[0]  # Highest resolution
            video_url = best_video.get('link')
            if video_url:
                all_video_urls.append(video_url)
            else:
                print(f"No valid URL found for video ID {video.get('id')}")

            if len(all_video_urls) >= videos_per_tag:
                break

        if len(all_video_urls) >= videos_per_tag:
            break

    if not all_video_urls:
        print(f"No video URLs found for tag '{tag}'. Please check your tags and API key.")
        return

    print(f"Found {len(all_video_urls)} videos for tag '{tag}'. Starting download...")

    def download_video(idx_url):
        idx, url = idx_url
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                video_path = os.path.join(download_path, f'video_{idx}.mp4')
                with open(video_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                print(f"Downloaded: {video_path}")
            else:
                print(f"Failed to download video from {url}. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading video from {url}: {e}")

    # Use ThreadPoolExecutor to download videos in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_video, enumerate(all_video_urls, start=1))

def select_best_clip(clip, duration=10):
    """
    Selects a subclip from the middle of the video clip.
    :param clip: MoviePy VideoFileClip object
    :param duration: Duration of the subclip in seconds
    :return: Subclip VideoFileClip object
    """
    if clip.duration <= duration:
        return clip
    start_time = (clip.duration - duration) / 2
    return clip.subclip(start_time, start_time + duration)

def merge_videos_to_match_audio(video_dir, audio_path, output_path, target_resolution=(1920, 1080)):
    """
    Merges multiple video clips to match the duration of the audio.

    :param video_dir: Directory containing video clips.
    :param audio_path: Path to the audio file.
    :param output_path: Path to save the merged video.
    :param target_resolution: Desired resolution for the output video.
    :return: Path to the merged video.
    """
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    if not video_files:
        print("No videos to merge.")
        return None

    # Load all video clips and select best subclips
    clips = []
    for vf in video_files:
        try:
            clip = VideoFileClip(vf)
            # Select a 10-second subclip from the middle
            best_clip = select_best_clip(clip, duration=10)
            # Resize to target resolution
            best_clip_resized = best_clip.resize(newsize=target_resolution)
            clips.append(best_clip_resized)
            print(f"Processed clip: {vf}")
        except Exception as e:
            print(f"Error processing video {vf}: {e}")

    if not clips:
        print("No valid clips to merge after processing.")
        return None

    # Load audio to get its duration
    try:
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration  # in seconds
        audio.close()
        print(f"Audio duration: {audio_duration} seconds")
    except Exception as e:
        print(f"Error loading audio file {audio_path}: {e}")
        return None

    # Calculate total duration of all clips
    total_clips_duration = sum(clip.duration for clip in clips)
    print(f"Total duration of available clips: {total_clips_duration} seconds")

    if total_clips_duration == 0:
        print("Total duration of clips is zero. Exiting.")
        return None

    # Determine how many times to loop the clips
    loops = int(audio_duration // total_clips_duration) + 1
    print(f"Looping video clips {loops} times to exceed audio duration.")

    # Concatenate clips multiple times
    final_clips = clips * loops
    try:
        concatenated = concatenate_videoclips(final_clips, method='compose')
    except Exception as e:
        print(f"Error concatenating clips: {e}")
        return None

    # Trim the video to match the audio duration
    try:
        trimmed = concatenated.subclip(0, audio_duration)
    except Exception as e:
        print(f"Error trimming the concatenated video: {e}")
        concatenated.close()
        return None

    # Write the trimmed video using GPU-accelerated codec
    try:
        trimmed.write_videofile(
            output_path,
            codec=FFMPEG_CODEC,
            bitrate=FFMPEG_CODEC_PARAMS['bitrate'],
            preset=FFMPEG_CODEC_PARAMS['preset'],
            threads=FFMPEG_CODEC_PARAMS['threads'],
            # preset_flags=FFMPEG_CODEC_PARAMS.get('preset_flags', None),  # Removed to fix TypeError
            audio=False,
            verbose=True,  # Set to True for more detailed output
            logger='bar'    # You can set it to 'bar', 'tqdm', etc.
        )
        print(f"Merged and trimmed video saved to {output_path}")
    except Exception as e:
        print(f"Error writing the merged video file: {e}")
    finally:
        trimmed.close()
        concatenated.close()
        # Close all individual clips
        for clip in clips:
            clip.close()

    return output_path

def add_audio_to_video(video_path, audio_path, output_path, target_resolution=(1920, 1080)):
    """
    Adds audio to the video and ensures the desired resolution.

    :param video_path: Path to the video file.
    :param audio_path: Path to the audio file.
    :param output_path: Path to save the final video with audio.
    :param target_resolution: Desired resolution for the output video.
    """
    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Set audio to video
        final_video = video.set_audio(audio)

        # Ensure the final video is at target resolution
        if final_video.size != target_resolution:
            final_video = final_video.resize(newsize=target_resolution)

        # Write the final video using GPU-accelerated codec
        final_video.write_videofile(
            output_path,
            codec=FFMPEG_CODEC,
            bitrate=FFMPEG_CODEC_PARAMS['bitrate'],
            preset=FFMPEG_CODEC_PARAMS['preset'],
            threads=FFMPEG_CODEC_PARAMS['threads'],
            # preset_flags=FFMPEG_CODEC_PARAMS.get('preset_flags', None),  # Removed to fix TypeError
            audio_codec='aac',
            verbose=True,  # Set to True for more detailed output
            logger='bar'    # You can set it to 'bar', 'tqdm', etc.
        )

        print(f"Final video with audio saved to {output_path}")
    except Exception as e:
        print(f"Error adding audio to video: {e}")
    finally:
        video.close()
        audio.close()
        final_video.close()

def process_single_mp3(mp3_path, output_video_dir):
    """
    Processes a single MP3 file to create a corresponding video.

    :param mp3_path: Path to the MP3 file.
    :param output_video_dir: Directory to save the final video.
    """
    # Extract the tag from the MP3 filename (without extension)
    tag = os.path.splitext(os.path.basename(mp3_path))[0]
    print(f"\nProcessing MP3: {mp3_path} with tag: '{tag}'")

    # Create a temporary directory for this MP3's video downloads
    temp_dir = os.path.join(TEMP_VIDEO_DIR, tag)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Step 1: Search and download videos based on the tag
    search_and_download_videos(PEXELS_API_KEY, tag, VIDEOS_PER_TAG, temp_dir)

    # Step 2: Merge videos to match the audio length
    merged_video_path = os.path.join(TEMP_VIDEO_DIR, MERGED_VIDEO_TEMPLATE.format(tag))
    merged_video = merge_videos_to_match_audio(temp_dir, mp3_path, merged_video_path)

    if not merged_video or not os.path.exists(merged_video_path):
        print(f"Merged video not found for tag '{tag}'. Skipping this MP3.")
        return

    # Step 3: Add audio to the merged video
    final_output_path = os.path.join(OUTPUT_VIDEO_DIR, FINAL_OUTPUT_TEMPLATE.format(tag))
    add_audio_to_video(merged_video_path, mp3_path, final_output_path)

    # Cleanup temporary files for this MP3
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
        if os.path.exists(merged_video_path):
            os.remove(merged_video_path)
    except Exception as e:
        print(f"Error during cleanup for tag '{tag}': {e}")

    print(f"Completed processing for MP3: {mp3_path}")

def main():
    # Ensure the output_video directory exists
    if not os.path.exists(OUTPUT_VIDEO_DIR):
        os.makedirs(OUTPUT_VIDEO_DIR)

    # Ensure the temporary video directory exists
    if not os.path.exists(TEMP_VIDEO_DIR):
        os.makedirs(TEMP_VIDEO_DIR)

    # Get all MP3 files from the mp3files directory
    mp3_files = [os.path.join(MP3_FILES_DIR, f) for f in os.listdir(MP3_FILES_DIR) if f.lower().endswith('.mp3')]

    if not mp3_files:
        print(f"No MP3 files found in the directory '{MP3_FILES_DIR}'. Exiting.")
        return

    print(f"Found {len(mp3_files)} MP3 files. Starting processing...")

    # Process each MP3 file sequentially
    for mp3_path in mp3_files:
        process_single_mp3(mp3_path, OUTPUT_VIDEO_DIR)

    # Optionally, remove the main temp_videos directory if empty
    try:
        if os.path.exists(TEMP_VIDEO_DIR) and not os.listdir(TEMP_VIDEO_DIR):
            shutil.rmtree(TEMP_VIDEO_DIR)
    except Exception as e:
        print(f"Error cleaning up main temporary directory: {e}")

    print("\nAll MP3 files have been processed successfully.")

if __name__ == "__main__":
    main()
