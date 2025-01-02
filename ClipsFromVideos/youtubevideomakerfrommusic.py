import os
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from yt_dlp import YoutubeDL

# Optional: Specify FFmpeg binary if not in PATH
# from moviepy.config import change_settings
# change_settings({"FFMPEG_BINARY": "/path/to/ffmpeg"})

# Configuration
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

def search_and_download_videos(tag, videos_per_tag, download_path):
    """
    Searches YouTube for videos matching the tag with Creative Commons license and downloads them.

    :param tag: Tag to search for.
    :param videos_per_tag: Number of videos to download.
    :param download_path: Directory to save downloaded videos.
    """
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Use ytsearch with the desired number of videos
    search_query = f"ytsearch{videos_per_tag * 2}:{tag}"  # Fetch more results to account for filtering
    print(f"\n🔍 Searching YouTube for tag: '{tag}' with query: '{search_query}'")

    def is_cc_license(info):
        """
        Filters videos to include only those with Creative Commons license.

        :param info: Video information dictionary.
        :return: True if the video has a Creative Commons license, False otherwise.
        """
        license_info = info.get('license')
        title = info.get('title', 'Unknown Title')
        
        if isinstance(license_info, str):
            if 'creative commons' in license_info.lower():
                print(f"✅ Video '{title}' has a Creative Commons license.")
                return True
            else:
                print(f"❌ Video '{title}' does not have a Creative Commons license.")
                return False
        else:
            print(f"❌ Video '{title}' does not have a license field or it's not a string.")
            return False

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(download_path, f'{tag}_%(id)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,  # Set to False to see yt-dlp logs; set to True to hide
        'ignoreerrors': True,
        'no_warnings': True,
        'retries': 3,
        'extract_flat': False,  # Set to False to retrieve full video info
        'match_filter': is_cc_license,
        # 'postprocessors': [{
        #     'key': 'FFmpegVideoConvertor',
        #     'preferredformat': 'mp4',  # Corrected spelling here
        # }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            # Perform the search and download
            print(f"🚀 Starting download of up to {videos_per_tag} CC-licensed videos for tag '{tag}'...")
            ydl.download([search_query])
            print(f"✅ Download completed for tag '{tag}'.")
        except Exception as e:
            print(f"⚠️ Error downloading videos for tag '{tag}': {e}")

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

def merge_videos_to_match_audio(video_dir, audio_path, output_path, target_resolution=(1920, 1080), min_video_duration=15):
    """
    Merges multiple video clips to match the duration of the audio.

    :param video_dir: Directory containing video clips.
    :param audio_path: Path to the audio file.
    :param output_path: Path to save the merged video.
    :param target_resolution: Desired resolution for the output video.
    :param min_video_duration: Minimum duration (in seconds) for a video to be considered valid.
    :return: Path to the merged video.
    """
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    if not video_files:
        print("❌ No videos to merge.")
        return None

    # Load all video clips and select best subclips
    clips = []
    for vf in video_files:
        try:
            clip = VideoFileClip(vf)
            if clip.duration < min_video_duration:
                print(f"⏩ Skipping video '{vf}' as it is shorter than {min_video_duration} seconds.")
                clip.close()
                continue
            # Select a 10-second subclip from the middle
            best_clip = select_best_clip(clip, duration=10)
            # Resize to target resolution
            best_clip_resized = best_clip.resize(newsize=target_resolution)
            clips.append(best_clip_resized)
            print(f"🎬 Processed clip: {vf}")
        except Exception as e:
            print(f"⚠️ Error processing video '{vf}': {e}")

    if not clips:
        print("❌ No valid clips to merge after processing.")
        return None

    # Load audio to get its duration
    try:
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration  # in seconds
        audio.close()
        print(f"🎵 Audio duration: {audio_duration} seconds")
    except Exception as e:
        print(f"⚠️ Error loading audio file '{audio_path}': {e}")
        return None

    # Calculate total duration of all clips
    total_clips_duration = sum(clip.duration for clip in clips)
    print(f"🕒 Total duration of available clips: {total_clips_duration} seconds")

    if total_clips_duration == 0:
        print("❌ Total duration of clips is zero. Exiting.")
        return None

    # Determine how many times to loop the clips
    loops = int(audio_duration // total_clips_duration) + 1
    print(f"🔁 Looping video clips {loops} times to exceed audio duration.")

    # Concatenate clips multiple times
    final_clips = clips * loops
    try:
        concatenated = concatenate_videoclips(final_clips, method='compose')
    except Exception as e:
        print(f"⚠️ Error concatenating clips: {e}")
        return None

    # Trim the video to match the audio duration
    try:
        trimmed = concatenated.subclip(0, audio_duration)
    except Exception as e:
        print(f"⚠️ Error trimming the concatenated video: {e}")
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
            audio=False,
            verbose=True,  # Set to True for more detailed output
            logger='bar'    # You can set it to 'bar', 'tqdm', etc.
        )
        print(f"✅ Merged and trimmed video saved to '{output_path}'")
    except Exception as e:
        print(f"⚠️ Error writing the merged video file: {e}")
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
            audio_codec='aac',
            verbose=True,  # Set to True for more detailed output
            logger='bar'    # You can set it to 'bar', 'tqdm', etc.
        )

        print(f"✅ Final video with audio saved to '{output_path}'")
    except Exception as e:
        print(f"⚠️ Error adding audio to video: {e}")
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
    print(f"\n🎧 Processing MP3: '{mp3_path}' with tag: '{tag}'")

    # Create a temporary directory for this MP3's video downloads
    temp_dir = os.path.join(TEMP_VIDEO_DIR, tag)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Step 1: Search and download videos based on the tag using YouTube
    search_and_download_videos(tag, VIDEOS_PER_TAG, temp_dir)

    # Step 2: Merge videos to match the audio length
    merged_video_path = os.path.join(TEMP_VIDEO_DIR, MERGED_VIDEO_TEMPLATE.format(tag))
    merged_video = merge_videos_to_match_audio(temp_dir, mp3_path, merged_video_path)

    if not merged_video or not os.path.exists(merged_video_path):
        print(f"❌ Merged video not found for tag '{tag}'. Skipping this MP3.")
        return

    # Step 3: Add audio to the merged video
    final_output_path = os.path.join(output_video_dir, FINAL_OUTPUT_TEMPLATE.format(tag))
    add_audio_to_video(merged_video_path, mp3_path, final_output_path)

    # Cleanup temporary files for this MP3
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
        if os.path.exists(merged_video_path):
            os.remove(merged_video_path)
    except Exception as e:
        print(f"⚠️ Error during cleanup for tag '{tag}': {e}")

    print(f"✅ Completed processing for MP3: '{mp3_path}'")

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
        print(f"❌ No MP3 files found in the directory '{MP3_FILES_DIR}'. Exiting.")
        return

    print(f"\n📂 Found {len(mp3_files)} MP3 file(s). Starting processing...")

    # Process each MP3 file sequentially
    for mp3_path in mp3_files:
        process_single_mp3(mp3_path, OUTPUT_VIDEO_DIR)

    # Optionally, remove the main temp_videos directory if empty
    try:
        if os.path.exists(TEMP_VIDEO_DIR) and not os.listdir(TEMP_VIDEO_DIR):
            shutil.rmtree(TEMP_VIDEO_DIR)
    except Exception as e:
        print(f"⚠️ Error cleaning up main temporary directory: {e}")

    print("\n🎉 All MP3 files have been processed successfully.")

if __name__ == "__main__":
    main()
