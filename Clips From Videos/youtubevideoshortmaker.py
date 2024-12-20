import os
import sys
import time
import logging
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from moviepy.editor import VideoFileClip, AudioFileClip

# ----------------------------- Configuration Variables ----------------------------- #

# Predefined tags for searching YouTube videos
TAGS = [
    "Krishna",
    "Murli",
    "Devotional"
]  # Add or modify tags as needed

# Path to the MP3 file to be used as audio in Shorts
MP3_FILE_PATH = 'murli.mp3'  # Replace with your MP3 file path

# Number of videos to download per tag
MAX_VIDEOS_PER_TAG = 2  # Adjust as needed

# Directories for downloads and outputs
DOWNLOAD_DIR = 'downloaded_videos'
SHORTS_DIR = 'youtube_shorts'

# YouTube Shorts specifications
SHORTS_WIDTH = 1080
SHORTS_HEIGHT = 1920
MAX_DURATION = 60  # in seconds

# Logging configuration
LOG_FILE = 'youtube_short_maker.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

# -------------------------------------------------------------------------------------- #

def validate_configuration():
    """
    Validates the configuration variables.
    """
    if not TAGS:
        logging.error("TAGS list is empty. Please add at least one tag.")
        sys.exit(1)
    
    if not os.path.isfile(MP3_FILE_PATH):
        logging.error(f"MP3 file not found at {MP3_FILE_PATH}")
        sys.exit(1)
    
    # Create directories if they do not exist
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(SHORTS_DIR, exist_ok=True)

def search_youtube_videos(tags, max_videos_per_tag=2, retries=3, delay=5):
    """
    Searches YouTube for videos based on predefined tags.

    :param tags: List of string tags to search for.
    :param max_videos_per_tag: Number of videos to download per tag.
    :param retries: Number of retry attempts for failed searches.
    :param delay: Delay (in seconds) between retries.
    :return: Set of unique YouTube video URLs.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'ignoreerrors': True,
        'extract_flat': 'in_playlist',
        'socket_timeout': 30,  # Increased timeout
    }

    video_urls = set()

    with YoutubeDL(ydl_opts) as ydl:
        for tag in tags:
            search_query = f"ytsearch{max_videos_per_tag}:{tag}"
            attempt = 0
            while attempt < retries:
                try:
                    logging.info(f"Searching for tag: '{tag}' (Attempt {attempt + 1})")
                    search_results = ydl.extract_info(search_query, download=False)
                    if 'entries' in search_results:
                        for entry in search_results['entries']:
                            if entry and 'url' in entry:
                                if entry['url'].startswith('http'):
                                    video_url = entry['url']
                                else:
                                    video_url = f"https://www.youtube.com/watch?v={entry['url']}"
                                video_urls.add(video_url)
                                logging.info(f"  Found video: {video_url}")
                    break  # Break out of retry loop if successful
                except DownloadError as e:
                    logging.warning(f"  DownloadError: {e}")
                except Exception as e:
                    logging.warning(f"  Error searching for tag '{tag}': {e}")
                attempt += 1
                if attempt < retries:
                    logging.info(f"  Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logging.error(f"  Failed to search for tag '{tag}' after {retries} attempts.\n")

    logging.info(f"\nTotal unique videos found: {len(video_urls)}\n")
    return video_urls

def download_videos(video_urls, download_path='downloaded_videos'):
    """
    Downloads videos from YouTube using yt_dlp.

    :param video_urls: Set of YouTube video URLs.
    :param download_path: Directory to save downloaded videos.
    :return: List of paths to downloaded video files.
    """
    downloaded_files = []
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        for url in video_urls:
            try:
                logging.info(f"Downloading video: {url}")
                info_dict = ydl.extract_info(url, download=True)
                if info_dict:
                    video_title = info_dict.get('title', 'video').replace('/', '_').replace('\\', '_')
                    ext = info_dict.get('ext', 'mp4')
                    filename = os.path.join(download_path, f"{video_title}.{ext}")
                    if os.path.exists(filename):
                        downloaded_files.append(filename)
                        logging.info(f"  Downloaded: {filename}")
                    else:
                        logging.warning(f"  Download failed or file does not exist: {filename}")
            except Exception as e:
                logging.error(f"  Failed to download {url}. Reason: {e}")

    logging.info(f"\nTotal videos downloaded: {len(downloaded_files)}\n")
    return downloaded_files

def create_youtube_short(video_path, audio_path, output_path='youtube_shorts'):
    """
    Creates a YouTube Short from a video by cropping and adding audio.

    :param video_path: Path to the source video.
    :param audio_path: Path to the MP3 audio file.
    :param output_path: Directory to save the short video.
    """
    try:
        logging.info(f"Processing video: {video_path}")
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # Calculate aspect ratios
        video_ratio = video.w / video.h
        shorts_ratio = SHORTS_WIDTH / SHORTS_HEIGHT

        # Determine new dimensions
        if video_ratio > shorts_ratio:
            # Video is wider, resize height to SHORTS_HEIGHT and adjust width accordingly
            new_height = SHORTS_HEIGHT
            new_width = int(new_height * video_ratio)
        else:
            # Video is taller or equal, resize width to SHORTS_WIDTH and adjust height accordingly
            new_width = SHORTS_WIDTH
            new_height = int(new_width / video_ratio)

        # Resize and crop to 9:16
        video_resized = video.resize(newsize=(new_width, new_height))
        video_cropped = video_resized.crop(
            width=SHORTS_WIDTH,
            height=SHORTS_HEIGHT,
            x_center=new_width / 2,
            y_center=new_height / 2
        )

        # Trim video to max_duration
        final_duration = min(video_cropped.duration, MAX_DURATION)
        video_final = video_cropped.subclip(0, final_duration)

        # Set the new audio
        audio_final = audio.subclip(0, final_duration)
        video_final = video_final.set_audio(audio_final)

        # Export the short
        video_title = os.path.splitext(os.path.basename(video_path))[0]
        output_file = os.path.join(output_path, f"{video_title}_short.mp4")
        video_final.write_videofile(
            output_file,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        logging.info(f"  Short created: {output_file}\n")
    except Exception as e:
        logging.error(f"  Failed to process {video_path}. Reason: {e}\n")

def main():
    """
    Main function to execute the workflow.
    """
    # Validate configuration
    validate_configuration()

    # Search YouTube for videos
    video_urls = search_youtube_videos(TAGS, max_videos_per_tag=MAX_VIDEOS_PER_TAG)

    if not video_urls:
        logging.error("No videos found for the given tags.")
        sys.exit(1)

    # Download videos
    downloaded_videos = download_videos(video_urls, download_path=DOWNLOAD_DIR)

    if not downloaded_videos:
        logging.error("No videos were downloaded.")
        sys.exit(1)

    # Create YouTube Shorts
    for video_file in downloaded_videos:
        create_youtube_short(video_file, MP3_FILE_PATH, output_path=SHORTS_DIR)

    logging.info("All YouTube Shorts have been created successfully.")

if __name__ == "__main__":
    main()
