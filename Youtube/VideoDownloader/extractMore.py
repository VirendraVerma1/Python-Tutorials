import yt_dlp
import csv
import os
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Sample YouTube URLs for testing
sample_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://youtu.be/9bZkp7q19f0",
    "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"
]

# Configuration Variables
OUTPUT_DIRECTORY = "video_info_csv"          # Directory to save CSV files
LOG_LEVEL = "INFO"                           # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
NUMBER_OF_THREADS = 4                        # Number of threads for parallel processing
URLS_FROM_FILE = "urls.txt"                  # Path to the file containing URLs (one per line)
USE_FILE_INPUT = False                       # Set to True to load URLs from a file instead of using the list above

# CSV File Names
VIDEOS_CSV = "videos.csv"

# Initialize threading lock for CSV operations
csv_lock = Lock()

# Setup logging
def setup_logging(log_level):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("video_info_extractor.log"),
            logging.StreamHandler()
        ]
    )

def load_existing_videos(csv_path):
    """
    Loads existing video data from the CSV into a dictionary.
    
    Args:
        csv_path (str): Path to the videos CSV file.
    
    Returns:
        dict: A dictionary mapping video_id to video metadata.
    """
    videos_dict = {}
    if not os.path.isfile(csv_path):
        logging.info(f"No existing CSV found at {csv_path}. A new one will be created.")
        return videos_dict
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                video_id = row.get('video_id')
                if video_id:
                    videos_dict[video_id] = row
        logging.info(f"Loaded {len(videos_dict)} existing videos from {csv_path}")
    except Exception as e:
        logging.error(f"Failed to load existing videos from {csv_path}: {e}")
    
    return videos_dict

def fetch_video_info(url):
    """
    Fetches video metadata using yt_dlp.
    
    Args:
        url (str): The YouTube video URL.
    
    Returns:
        dict or None: Video metadata dictionary or None if extraction fails.
    """
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)

            # Prepare video metadata
            video_metadata = {
                'video_id': info_dict.get('id'),
                'title': info_dict.get('title'),
                'uploader': info_dict.get('uploader'),
                'upload_date': info_dict.get('upload_date'),
                'duration': info_dict.get('duration'),
                'view_count': info_dict.get('view_count'),
                'like_count': info_dict.get('like_count'),
                'dislike_count': info_dict.get('dislike_count'),
                'average_rating': info_dict.get('average_rating'),
                'subtitles': ';'.join(info_dict.get('subtitles', {}).keys()) if info_dict.get('subtitles') else '',
                'tags': ';'.join(info_dict.get('tags', [])) if info_dict.get('tags') else '',
                'categories': ';'.join(info_dict.get('categories', [])) if info_dict.get('categories') else '',
                'is_live': info_dict.get('is_live'),
                'is_private': info_dict.get('is_private'),
                'is_unlisted': info_dict.get('is_unlisted'),
                'webpage_url': info_dict.get('webpage_url'),
                'release_timestamp': info_dict.get('release_timestamp'),
                'channel_id': info_dict.get('channel_id'),
                'channel_url': info_dict.get('channel_url'),
                '__description__': "This CSV contains metadata extracted from the YouTube video using yt_dlp.",
                '__fetch_time__': datetime.utcnow().isoformat() + 'Z',
                '__source__': "yt_dlp Python library",
                '__notes__': "Fields like 'dislike_count' may not be available as YouTube has deprecated them.",
            }

            logging.info(f"Successfully fetched data for URL: {url}")
            return video_metadata

        except yt_dlp.utils.DownloadError as e:
            logging.error(f"DownloadError for URL {url}: {e}")
            return None
        except yt_dlp.utils.ExtractorError as e:
            logging.error(f"ExtractorError for URL {url}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error for URL {url}: {e}")
            return None

def update_videos_dict(videos_dict, video_data):
    """
    Updates the videos dictionary with new video data.
    
    Args:
        videos_dict (dict): Existing videos dictionary.
        video_data (dict): New video metadata to update or add.
    """
    video_id = video_data.get('video_id')
    if not video_id:
        logging.warning("Video data without a video_id encountered. Skipping.")
        return

    if video_id in videos_dict:
        logging.info(f"Updating existing video entry for video_id: {video_id}")
    else:
        logging.info(f"Adding new video entry for video_id: {video_id}")
    videos_dict[video_id] = video_data

def write_videos_to_csv(videos_dict, csv_path):
    """
    Writes the videos dictionary back to the CSV file.
    
    Args:
        videos_dict (dict): Dictionary containing all video metadata.
        csv_path (str): Path to the videos CSV file.
    """
    fieldnames = [
        'video_id', 'title', 'uploader', 'upload_date', 'duration', 'view_count',
        'like_count', 'dislike_count', 'average_rating', 'subtitles', 'tags',
        'categories', 'is_live', 'is_private', 'is_unlisted', 'webpage_url',
        'release_timestamp', 'channel_id', 'channel_url', '__description__',
        '__fetch_time__', '__source__', '__notes__'
    ]

    try:
        with csv_lock:
            with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for video_id, video_data in videos_dict.items():
                    writer.writerow(video_data)
        logging.info(f"Successfully wrote {len(videos_dict)} video entries to {csv_path}")
    except Exception as e:
        logging.error(f"Failed to write videos to CSV {csv_path}: {e}")

def load_urls_from_file(file_path):
    """
    Loads video URLs from a given text file, one URL per line.
    
    Args:
        file_path (str): Path to the text file containing URLs.
    
    Returns:
        list: A list of video URLs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        logging.info(f"Loaded {len(urls)} URLs from {file_path}")
        return urls
    except Exception as e:
        logging.error(f"Failed to load URLs from {file_path}: {e}")
        return []

def process_url(url, videos_dict):
    """
    Processes a single URL: fetches video info and updates the videos dictionary.
    
    Args:
        url (str): The video URL.
        videos_dict (dict): The shared videos dictionary to update.
    """
    video_data = fetch_video_info(url)
    if video_data:
        with csv_lock:
            update_videos_dict(videos_dict, video_data)
    else:
        logging.warning(f"Failed to extract information for URL: {url}")

def main():
    # Setup logging
    setup_logging(LOG_LEVEL.upper())

    # Define path for CSV file
    videos_csv_path = os.path.join(OUTPUT_DIRECTORY, VIDEOS_CSV)

    # Create output directory
    try:
        os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
        logging.info(f"Output directory '{OUTPUT_DIRECTORY}' is ready.")
    except Exception as e:
        logging.error(f"Failed to create directory '{OUTPUT_DIRECTORY}': {e}")
        return

    # Load existing videos into a dictionary
    videos_dict = load_existing_videos(videos_csv_path)

    # Gather video URLs
    video_urls = []
    if USE_FILE_INPUT:
        video_urls.extend(load_urls_from_file(URLS_FROM_FILE))
    else:
        video_urls.extend(sample_urls)

    if not video_urls:
        logging.error("No video URLs provided. Please add URLs to the script or specify a valid file.")
        return

    # Process URLs in parallel and update videos_dict
    with ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
        futures = [
            executor.submit(process_url, url, videos_dict)
            for url in video_urls
        ]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                # This should not occur as exceptions are handled in process_url
                logging.error(f"A thread generated an exception: {exc}")

    # After all URLs are processed, write the updated videos_dict back to CSV
    write_videos_to_csv(videos_dict, videos_csv_path)

    logging.info("Video information extraction process finished.")

if __name__ == "__main__":
    main()
