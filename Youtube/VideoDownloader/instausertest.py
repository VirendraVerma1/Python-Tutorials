import instaloader
import csv
from datetime import datetime
import os

def fetch_all_posts(username, output_csv='instagram_posts.csv', download_media=False, media_dir='media'):
    """
    Fetches all posts from a public Instagram profile and saves the information to a CSV file.
    
    Parameters:
    - username (str): Instagram username to fetch posts from.
    - output_csv (str): Filename for the output CSV.
    - download_media (bool): Whether to download media (images/videos).
    - media_dir (str): Directory to save downloaded media.
    """
    # Initialize Instaloader
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )
    
    try:
        # Load the profile without logging in
        profile = instaloader.Profile.from_username(loader.context, username)
        print(f"Fetching posts for profile: {profile.username}")
        print(profile)
        
        # Prepare CSV file
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Post URL', 'Shortcode', 'Date', 'Caption', 'Media Type',
                'Media URL', 'Likes', 'Comments'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Create media directory if downloading media
            if download_media:
                if not os.path.exists(media_dir):
                    os.makedirs(media_dir)
                print(f"Media will be downloaded to the '{media_dir}' directory.")
            
            # Iterate over all posts
            for post in profile.get_posts():
                print(post)
                post_url = f"https://www.instagram.com/p/{post.shortcode}/"
                shortcode = post.shortcode
                date = post.date_utc.strftime('%Y-%m-%d %H:%M:%S')
                caption = post.caption.replace('\n', ' ').replace('\r', ' ') if post.caption else ''
                likes = post.likes
                comments = post.comments
                media_type = 'Image' if post.is_video == False else 'Video'
                media_url = post.url if media_type == 'Image' else post.video_url
                
                # Write to CSV
                writer.writerow({
                    'Post URL': post_url,
                    'Shortcode': shortcode,
                    'Date': date,
                    'Caption': caption,
                    'Media Type': media_type,
                    'Media URL': media_url,
                    'Likes': likes,
                    'Comments': comments
                })
                
                print(f"Fetched post: {post_url}")
                
                # Download media if required
                if download_media:
                    try:
                        if media_type == 'Image':
                            loader.download_url(
                                url=media_url,
                                filename=os.path.join(media_dir, f"{shortcode}.jpg")
                            )
                        elif media_type == 'Video':
                            loader.download_url(
                                url=media_url,
                                filename=os.path.join(media_dir, f"{shortcode}.mp4")
                            )
                        print(f"Downloaded media for post: {post_url}")
                    except Exception as e:
                        print(f"Failed to download media for post {post_url}: {e}")
        
        print(f"All posts have been fetched and saved to '{output_csv}'.")
        if download_media:
            print(f"All media files have been downloaded to the '{media_dir}' directory.")
    
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"The profile '{username}' does not exist.")
    except instaloader.exceptions.ConnectionException as ce:
        print("Connection error:", ce)
    except Exception as e:
        print("An unexpected error occurred:", e)

# Example usage
if __name__ == "__main__":
    instagram_username = "freepressjournal"
    output_csv_file = "freepressjournal_posts.csv"
    download_media_files = False  # Set to True to download images/videos
    media_directory = "freepressjournal_media"
    
    fetch_all_posts(
        username=instagram_username,
        output_csv=output_csv_file,
        download_media=download_media_files,
        media_dir=media_directory
    )
