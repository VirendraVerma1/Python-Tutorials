import instaloader
import csv
from datetime import datetime
import os

def initialize_instaloader():
    """
    Initialize and return an Instaloader instance with default settings.
    """
    return instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )

def get_profile(loader, username):
    """
    Retrieve an Instagram profile.
    
    Parameters:
    - loader (instaloader.Instaloader): Initialized Instaloader instance
    - username (str): Instagram username to fetch
    
    Returns:
    - instaloader.Profile: Profile object
    """
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        print(f"Successfully loaded profile: {profile.username}")
        return profile
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"The profile '{username}' does not exist.")
        raise
    except instaloader.exceptions.ConnectionException as ce:
        print("Connection error:", ce)
        raise

def prepare_csv_file(filename):
    """
    Create and prepare a CSV file with headers.
    
    Parameters:
    - filename (str): Name of the CSV file to create
    
    Returns:
    - tuple: (csv file object, csv writer object)
    """
    csvfile = open(filename, mode='w', newline='', encoding='utf-8')
    fieldnames = [
        'Post URL', 'Shortcode', 'Date', 'Caption', 'Media Type',
        'Media URL', 'Likes', 'Comments'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    return csvfile, writer

def extract_post_data(post):
    """
    Extract relevant data from a post.
    
    Parameters:
    - post (instaloader.Post): Post object
    
    Returns:
    - dict: Dictionary containing post data
    """
    return {
        'Post URL': f"https://www.instagram.com/p/{post.shortcode}/",
        'Shortcode': post.shortcode,
        'Date': post.date_utc.strftime('%Y-%m-%d %H:%M:%S'),
        'Caption': post.caption.replace('\n', ' ').replace('\r', ' ') if post.caption else '',
        'Media Type': 'Video' if post.is_video else 'Image',
        'Media URL': post.video_url if post.is_video else post.url,
        'Likes': post.likes,
        'Comments': post.comments
    }

def download_media_file(loader, post_data, media_dir):
    """
    Download media file from a post.
    
    Parameters:
    - loader (instaloader.Instaloader): Initialized Instaloader instance
    - post_data (dict): Dictionary containing post data
    - media_dir (str): Directory to save media files
    """
    try:
        extension = '.mp4' if post_data['Media Type'] == 'Video' else '.jpg'
        filename = os.path.join(media_dir, f"{post_data['Shortcode']}{extension}")
        loader.download_url(url=post_data['Media URL'], filename=filename)
        print(f"Downloaded media for post: {post_data['Post URL']}")
    except Exception as e:
        print(f"Failed to download media for post {post_data['Post URL']}: {e}")

def fetch_all_posts(username, output_csv='instagram_posts.csv', download_media=False, media_dir='media'):
    """
    Main function to fetch all posts from a public Instagram profile.
    
    Parameters:
    - username (str): Instagram username to fetch posts from
    - output_csv (str): Filename for the output CSV
    - download_media (bool): Whether to download media files
    - media_dir (str): Directory to save downloaded media
    """
    loader = initialize_instaloader()
    
    try:
        # Get profile and prepare CSV
        profile = get_profile(loader, username)
        csvfile, writer = prepare_csv_file(output_csv)
        
        # Create media directory if needed
        if download_media:
            os.makedirs(media_dir, exist_ok=True)
            print(f"Media will be downloaded to the '{media_dir}' directory.")
        
        # Process posts
        with csvfile:
            for post in profile.get_posts():
                post_data = extract_post_data(post)
                writer.writerow(post_data)
                print(f"Fetched post: {post_data['Post URL']}")
                
                if download_media:
                    download_media_file(loader, post_data, media_dir)
        
        print(f"All posts have been fetched and saved to '{output_csv}'.")
        if download_media:
            print(f"All media files have been downloaded to the '{media_dir}' directory.")
            
    except Exception as e:
        print("An error occurred:", e)
        raise

if __name__ == "__main__":
    instagram_username = "freepressjournal"
    output_csv_file = "freepressjournal_posts.csv"
    download_media_files = False
    media_directory = "freepressjournal_media"
    
    fetch_all_posts(
        username=instagram_username,
        output_csv=output_csv_file,
        download_media=download_media_files,
        media_dir=media_directory
    )