import instaloader
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import logging
import signal
import sys

# --------------------------- Configuration ---------------------------

# Replace these with your Instagram credentials or set them as environment variables
USERNAME = os.getenv('INSTAGRAM_USERNAME', 'gesab36114')
PASSWORD = os.getenv('INSTAGRAM_PASSWORD', '$2$aYWf&2!fAHnU')

# CSV file paths
USERS_CSV = 'users.csv'
POSTS_CSV = 'posts.csv'
LIKES_CSV = 'likes.csv'
COMMENTS_CSV = 'comments.csv'
BLOCKED_USERS_CSV = 'blocked_users.csv'  # To track blocked users

# Date format used in users.csv
DATE_FORMAT = '%Y-%m-%d'

# Rate limiting configuration
INITIAL_SLEEP_INTERVAL = 15    # Increased from 5 to 15 seconds
MAX_SLEEP_INTERVAL = 600       # Increased from 300 to 600 seconds (10 minutes)
MAX_RETRIES = 3                # Reduced from 5 to 3

# Logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("instabot.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# --------------------------------------------------------------------

def signal_handler(sig, frame):
    logging.info('Interrupt received. Exiting gracefully.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def authenticate_instaloader(username: str, password: str) -> instaloader.Instaloader:
    """
    Authenticates and returns an Instaloader instance.
    Handles Two-Factor Authentication (2FA) if enabled.
    """
    loader = instaloader.Instaloader()
    try:
        loader.login(username, password)
        logging.info("Logged in successfully.")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        two_factor_code = input("Enter 2FA code: ")
        try:
            loader.login(username, password, two_factor_code)
            logging.info("Logged in successfully with 2FA.")
        except Exception as e:
            logging.error(f"Failed to login with 2FA: {e}")
            exit(1)
    except instaloader.exceptions.BadCredentialsException:
        logging.error("Incorrect username or password.")
        exit(1)
    except instaloader.exceptions.ConnectionException as e:
        logging.error(f"Connection error during login: {e}")
        exit(1)
    except Exception as e:
        logging.error(f"Login failed: {e}")
        exit(1)
    return loader

def load_existing_ids(file_path: str, id_column: str) -> set:
    """
    Loads existing IDs from a CSV file into a set for quick lookup.
    """
    if not os.path.exists(file_path):
        logging.warning(f"{file_path} not found. Starting with an empty set.")
        return set()
    
    try:
        df = pd.read_csv(file_path, usecols=[id_column])
        existing_ids = set(df[id_column].dropna().astype(int).tolist())
        logging.info(f"Loaded {len(existing_ids)} existing IDs from {file_path}.")
        return existing_ids
    except Exception as e:
        logging.error(f"Error loading {file_path}: {e}")
        return set()

def load_users(users_csv: str) -> pd.DataFrame:
    """
    Loads users.csv into a DataFrame, ensuring correct data types.
    If the file does not exist, creates it with all possible columns.
    """
    required_columns = [
        'username', 'user_id', 'full_name', 'biography',
        'followers_count', 'following_count', 'is_private',
        'is_verified', 'profile_pic_url', 'last_scanned_date'
    ]
    
    if not os.path.exists(users_csv):
        logging.warning(f"{users_csv} not found. Creating a new DataFrame with all columns.")
        users_df = pd.DataFrame(columns=required_columns)
        # Use pandas nullable boolean dtype
        users_df['is_private'] = users_df['is_private'].astype('boolean')
        users_df['is_verified'] = users_df['is_verified'].astype('boolean')
        users_df.to_csv(users_csv, index=False)
        return users_df
    
    try:
        users_df = pd.read_csv(users_csv, dtype={
            'username': str,
            'user_id': float,
            'full_name': str,
            'biography': str,
            'followers_count': float,
            'following_count': float,
            'is_private': 'boolean',  # Nullable boolean
            'is_verified': 'boolean',  # Nullable boolean
            'profile_pic_url': str,
            'last_scanned_date': str
        })
        logging.info(f"Loaded {len(users_df)} users from {users_csv}.")
        # Ensure all necessary columns exist
        for col in required_columns:
            if col not in users_df.columns:
                if col in ['is_private', 'is_verified']:
                    users_df[col] = pd.NA
                    users_df[col] = users_df[col].astype('boolean')
                else:
                    users_df[col] = None
                logging.info(f"Added missing column '{col}' to {users_csv}.")
        return users_df
    except Exception as e:
        logging.error(f"Error loading {users_csv}: {e}")
        # Attempt to create a new CSV with required columns
        users_df = pd.DataFrame(columns=required_columns)
        users_df['is_private'] = users_df['is_private'].astype('boolean')
        users_df['is_verified'] = users_df['is_verified'].astype('boolean')
        users_df.to_csv(users_csv, index=False)
        return users_df

def append_to_csv(file_path: str, data: dict, columns: list):
    """
    Appends a single row to a CSV file.
    Ensures that all necessary columns exist.
    """
    df = pd.DataFrame([data])
    # Check if file exists
    file_exists = os.path.isfile(file_path)
    if not file_exists:
        # Create file with headers and appropriate dtypes
        if file_path == USERS_CSV:
            for col in columns:
                if col in ['is_private', 'is_verified']:
                    df[col] = df[col].astype('boolean')
        df.to_csv(file_path, mode='w', header=True, index=False)
        logging.info(f"Created new {file_path} with data: {data}")
    else:
        try:
            existing_columns = pd.read_csv(file_path, nrows=0).columns.tolist()
            # Determine missing columns
            missing_columns = [col for col in columns if col not in existing_columns]
            for col in missing_columns:
                df[col] = None  # Assign None to missing columns
                if col in ['is_private', 'is_verified']:
                    df[col] = df[col].astype('boolean')
                logging.info(f"Added missing column '{col}' to {file_path}.")
            # Reorder columns to match the existing CSV
            ordered_columns = existing_columns + [col for col in df.columns if col not in existing_columns]
            df = df[ordered_columns]
            # Append to CSV
            df.to_csv(file_path, mode='a', header=False, index=False)
            logging.info(f"Appended data to {file_path}: {data}")
        except Exception as e:
            logging.error(f"Failed to append data to {file_path}: {e}")

def is_scan_required(last_scanned_str: str, cutoff_date: datetime) -> bool:
    """
    Determines if a user's data needs to be scanned based on the last scanned date.
    """
    if pd.isna(last_scanned_str):
        logging.info("last_scanned_date is missing. Scan is required.")
        return True  # Force scan if date is missing

    try:
        last_scanned_date = datetime.strptime(last_scanned_str, DATE_FORMAT)
    except Exception as e:
        logging.warning(f"Error parsing date '{last_scanned_str}': {e}. Scan is required.")
        return True  # Force scan if date parsing fails
    return last_scanned_date < cutoff_date

def fetch_profile(loader: instaloader.Instaloader, user_id: int) -> instaloader.Profile:
    """
    Fetches an Instagram profile using Instaloader.
    """
    try:
        profile = instaloader.Profile.from_id(loader.context, user_id)
        return profile
    except instaloader.exceptions.ProfileNotExistsException:
        logging.error(f"No profile found for user ID {user_id}. The user may have blocked you.")
        add_blocked_user(user_id)
        return None
    except instaloader.exceptions.InstaloaderException as e:
        logging.error(f"Instaloader exception for user ID {user_id}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching profile for user ID {user_id}: {e}")
        return None

def fetch_user_id(loader: instaloader.Instaloader, username: str) -> int:
    """
    Fetches the Instagram user ID for a given username.
    """
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        return profile.userid
    except instaloader.exceptions.ProfileNotExistsException:
        logging.error(f"Username '{username}' does not exist.")
        return None
    except instaloader.exceptions.InstaloaderException as e:
        logging.error(f"Instaloader exception while fetching user ID for '{username}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching user ID for '{username}': {e}")
        return None

def add_blocked_user(user_id: int):
    """
    Adds a user ID to blocked_users.csv to prevent future processing.
    """
    blocked_user_data = {
        'user_id': user_id,
        'blocked_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    columns = ['user_id', 'blocked_at']
    append_to_csv(BLOCKED_USERS_CSV, blocked_user_data, columns)
    logging.info(f"Added user ID {user_id} to {BLOCKED_USERS_CSV}.")

def add_user_if_new(loader: instaloader.Instaloader, users_set: set, users_csv: str, username: str, user_id: int):
    """
    Adds a new user to the users.csv if the user_id is not already present.
    Fetches additional user information.
    """
    if user_id not in users_set:
        try:
            profile = instaloader.Profile.from_id(loader.context, user_id)
            # Handle cases where certain attributes might be missing
            full_name = profile.full_name if hasattr(profile, 'full_name') else None
            biography = profile.biography if hasattr(profile, 'biography') else None
            followers_count = profile.followers if hasattr(profile, 'followers') else None
            following_count = profile.followees if hasattr(profile, 'followees') else None
            is_private = profile.is_private if hasattr(profile, 'is_private') else None
            is_verified = profile.is_verified if hasattr(profile, 'is_verified') else None
            profile_pic_url = profile.profile_pic_url if hasattr(profile, 'profile_pic_url') else None

            user_data = {
                'username': profile.username,
                'user_id': profile.userid,
                'full_name': full_name,
                'biography': biography,
                'followers_count': followers_count,
                'following_count': following_count,
                'is_private': is_private,
                'is_verified': is_verified,
                'profile_pic_url': profile_pic_url,
                'last_scanned_date': '1970-01-01'  # Default date
            }
            append_to_csv(users_csv, user_data, [
                'username', 'user_id', 'full_name', 'biography',
                'followers_count', 'following_count', 'is_private',
                'is_verified', 'profile_pic_url', 'last_scanned_date'
            ])
            users_set.add(user_id)
            logging.info(f"Added new user {profile.username} to {users_csv}.")
        except instaloader.exceptions.ProfileNotExistsException:
            logging.error(f"No profile found for user ID {user_id}. The user may have blocked you.")
            add_blocked_user(user_id)
        except instaloader.exceptions.InstaloaderException as e:
            logging.error(f"Instaloader exception while adding new user ID {user_id}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error while adding new user ID {user_id}: {e}")

def process_likes(loader: instaloader.Instaloader, post, post_id: int, likes_set: set, likes_csv: str, users_set: set, users_csv: str):
    """
    Processes likes on a post, appending new likes to likes.csv and adding new users.
    Fetches additional liker information.
    """
    try:
        likes = post.get_likes()
        for like in likes:
            liker_id = like.userid
            if liker_id not in likes_set:
                liker_profile = like
                # Handle cases where certain attributes might be missing
                username = liker_profile.username if hasattr(liker_profile, 'username') else None
                full_name = liker_profile.full_name if hasattr(liker_profile, 'full_name') else None
                profile_pic_url = liker_profile.profile_pic_url if hasattr(liker_profile, 'profile_pic_url') else None
                is_verified = liker_profile.is_verified if hasattr(liker_profile, 'is_verified') else None

                like_data = {
                    'post_id': post_id,
                    'user_id': liker_id,
                    'username': username,
                    'full_name': full_name,
                    'profile_pic_url': profile_pic_url,
                    'is_verified': is_verified
                }
                append_to_csv(likes_csv, like_data, [
                    'post_id', 'user_id', 'username', 'full_name',
                    'profile_pic_url', 'is_verified'
                ])
                likes_set.add(liker_id)
                logging.info(f"Added like from user_id {liker_id} on post {post_id}.")
                # Add liker to users.csv if not present
                add_user_if_new(loader, users_set, users_csv, username, liker_id)
    except instaloader.exceptions.InstaloaderException as e:
        if "401 Unauthorized" in str(e) or "429 Too Many Requests" in str(e):
            logging.error(f"{e.__class__.__name__}: {e}")
            raise e  # Propagate exception to trigger retry
        else:
            logging.error(f"Instaloader exception while fetching likes for post {post_id}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while fetching likes for post {post_id}: {e}")

def process_comments(loader: instaloader.Instaloader, post, post_id: int, comments_set: set, comments_csv: str, users_set: set, users_csv: str):
    """
    Processes comments on a post, appending new comments to comments.csv and adding new users.
    Fetches additional commenter information.
    """
    try:
        comments = post.get_comments()
        for comment in comments:
            commenter_id = comment.owner.userid
            if commenter_id not in comments_set:
                commenter_profile = comment.owner
                # Handle cases where certain attributes might be missing
                username = commenter_profile.username if hasattr(commenter_profile, 'username') else None
                full_name = commenter_profile.full_name if hasattr(commenter_profile, 'full_name') else None
                profile_pic_url = commenter_profile.profile_pic_url if hasattr(commenter_profile, 'profile_pic_url') else None
                is_verified = commenter_profile.is_verified if hasattr(commenter_profile, 'is_verified') else None

                comment_data = {
                    'post_id': post_id,
                    'user_id': commenter_id,
                    'username': username,
                    'full_name': full_name,
                    'profile_pic_url': profile_pic_url,
                    'is_verified': is_verified,
                    'comment_id': comment.id,
                    'text': comment.text,
                    'created_at': datetime.fromtimestamp(comment.created_at_utc).strftime('%Y-%m-%d %H:%M:%S')
                }
                append_to_csv(comments_csv, comment_data, [
                    'post_id', 'user_id', 'username', 'full_name',
                    'profile_pic_url', 'is_verified', 'comment_id',
                    'text', 'created_at'
                ])
                comments_set.add(commenter_id)
                logging.info(f"Added comment from user_id {commenter_id} on post {post_id}.")
                # Add commenter to users.csv if not present
                add_user_if_new(loader, users_set, users_csv, username, commenter_id)
    except instaloader.exceptions.InstaloaderException as e:
        if "401 Unauthorized" in str(e) or "429 Too Many Requests" in str(e):
            logging.error(f"{e.__class__.__name__}: {e}")
            raise e  # Propagate exception to trigger retry
        else:
            logging.error(f"Instaloader exception while fetching comments for post {post_id}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while fetching comments for post {post_id}: {e}")

def process_posts(loader: instaloader.Instaloader, profile: instaloader.Profile, user_id: int,
                 posts_set: set, posts_csv: str,
                 likes_set: set, likes_csv: str,
                 comments_set: set, comments_csv: str,
                 users_set: set, users_csv: str):
    """
    Processes all posts of a user, appending new posts, likes, and comments to their respective CSVs.
    Implements retry mechanism for handling rate limiting.
    """
    for post in profile.get_posts():
        post_id = post.mediaid

        # Check if post already exists
        if post_id not in posts_set:
            post_data = {
                'user_id': user_id,
                'post_id': post_id,
                'shortcode': post.shortcode,
                'caption': post.caption,
                'media_type': post.typename,
                'media_url': post.url,
                'likes_count': post.likes,
                'comments_count': post.comments,
                'taken_at': post.date_utc.strftime('%Y-%m-%d %H:%M:%S'),
                'location': post.location.name if post.location else None
            }
            append_to_csv(posts_csv, post_data, [
                'user_id', 'post_id', 'shortcode', 'caption', 'media_type',
                'media_url', 'likes_count', 'comments_count', 'taken_at', 'location'
            ])
            posts_set.add(post_id)
            logging.info(f"Added post {post_id} for user {profile.username}.")

        # Process likes with retry mechanism
        retry_count = 0
        sleep_interval = INITIAL_SLEEP_INTERVAL

        while retry_count < MAX_RETRIES:
            try:
                process_likes(loader, post, post_id, likes_set, likes_csv, users_set, users_csv)
                break  # Exit the retry loop if successful
            except instaloader.exceptions.InstaloaderException as e:
                if "401 Unauthorized" in str(e) or "429 Too Many Requests" in str(e):
                    logging.error(f"{e.__class__.__name__}: {e}")
                    logging.info(f"Sleeping for {sleep_interval} seconds before retrying likes.")
                    time.sleep(sleep_interval)
                    retry_count += 1
                    sleep_interval = min(sleep_interval * 2, MAX_SLEEP_INTERVAL)
                else:
                    logging.error(f"Instaloader exception while fetching likes for post {post_id}: {e}")
                    break
            except Exception as e:
                logging.error(f"Unexpected error while fetching likes for post {post_id}: {e}")
                break

        # Process comments with retry mechanism
        retry_count = 0
        sleep_interval = INITIAL_SLEEP_INTERVAL

        while retry_count < MAX_RETRIES:
            try:
                process_comments(loader, post, post_id, comments_set, comments_csv, users_set, users_csv)
                break  # Exit the retry loop if successful
            except instaloader.exceptions.InstaloaderException as e:
                if "401 Unauthorized" in str(e) or "429 Too Many Requests" in str(e):
                    logging.error(f"{e.__class__.__name__}: {e}")
                    logging.info(f"Sleeping for {sleep_interval} seconds before retrying comments.")
                    time.sleep(sleep_interval)
                    retry_count += 1
                    sleep_interval = min(sleep_interval * 2, MAX_SLEEP_INTERVAL)
                else:
                    logging.error(f"Instaloader exception while fetching comments for post {post_id}: {e}")
                    break
            except Exception as e:
                logging.error(f"Unexpected error while fetching comments for post {post_id}: {e}")
                break

        # Respect rate limits
        logging.debug(f"Sleeping for {INITIAL_SLEEP_INTERVAL} seconds to respect rate limits.")
        time.sleep(INITIAL_SLEEP_INTERVAL)

def update_last_scanned(users_csv: str, username: str, current_date: str):
    """
    Updates the last_scanned_date for a user in users.csv.
    """
    # Read the entire users.csv
    try:
        users_df = pd.read_csv(users_csv, dtype={
            'username': str,
            'user_id': float,
            'full_name': str,
            'biography': str,
            'followers_count': float,
            'following_count': float,
            'is_private': 'boolean',
            'is_verified': 'boolean',
            'profile_pic_url': str,
            'last_scanned_date': str
        })
    except Exception as e:
        logging.error(f"Failed to read {users_csv} for updating last_scanned_date: {e}")
        return

    # Update the specific user's last_scanned_date
    try:
        users_df.loc[users_df['username'] == username, 'last_scanned_date'] = current_date
        users_df.to_csv(users_csv, index=False)
        logging.info(f"Updated last_scanned_date for user {username} to {current_date}.")
    except Exception as e:
        logging.error(f"Failed to update last_scanned_date for user {username}: {e}")

def main():
    """
    Main function to orchestrate the data fetching and CSV updating process.
    """
    # Initialize Instaloader and authenticate
    loader = authenticate_instaloader(USERNAME, PASSWORD)

    # Load existing IDs into sets
    users_df = load_users(USERS_CSV)
    users_set = set(users_df['user_id'].dropna().astype(int).tolist())

    posts_set = load_existing_ids(POSTS_CSV, 'post_id')
    likes_set = load_existing_ids(LIKES_CSV, 'user_id')
    comments_set = load_existing_ids(COMMENTS_CSV, 'user_id')

    # Load blocked users to prevent reprocessing
    blocked_users_set = load_existing_ids(BLOCKED_USERS_CSV, 'user_id')

    # Define the cutoff date (6 months ago)
    cutoff_date = datetime.now() - timedelta(days=180)

    # Iterate through each user in users.csv
    for index, row in users_df.iterrows():
        username = row['username']
        user_id = row['user_id']
        last_scanned_str = row['last_scanned_date']

        logging.info(f"\nProcessing user: {username} (ID: {user_id})")

        # Check if user_id is missing or invalid
        if pd.isna(user_id):
            logging.warning(f"user_id missing for {username}. Attempting to fetch user_id.")
            fetched_user_id = fetch_user_id(loader, username)
            if fetched_user_id:
                # Check if user is blocked
                if fetched_user_id in blocked_users_set:
                    logging.warning(f"User ID {fetched_user_id} is in {BLOCKED_USERS_CSV}. Skipping.")
                    continue

                # Append the new user to users.csv with full information
                try:
                    profile = instaloader.Profile.from_id(loader.context, fetched_user_id)
                    # Handle cases where certain attributes might be missing
                    full_name = profile.full_name if hasattr(profile, 'full_name') else None
                    biography = profile.biography if hasattr(profile, 'biography') else None
                    followers_count = profile.followers if hasattr(profile, 'followers') else None
                    following_count = profile.followees if hasattr(profile, 'followees') else None
                    is_private = profile.is_private if hasattr(profile, 'is_private') else None
                    is_verified = profile.is_verified if hasattr(profile, 'is_verified') else None
                    profile_pic_url = profile.profile_pic_url if hasattr(profile, 'profile_pic_url') else None

                    user_data = {
                        'username': profile.username,
                        'user_id': profile.userid,
                        'full_name': full_name,
                        'biography': biography,
                        'followers_count': followers_count,
                        'following_count': following_count,
                        'is_private': is_private,
                        'is_verified': is_verified,
                        'profile_pic_url': profile_pic_url,
                        'last_scanned_date': '1970-01-01'  # Default date
                    }
                    append_to_csv(USERS_CSV, user_data, [
                        'username', 'user_id', 'full_name', 'biography',
                        'followers_count', 'following_count', 'is_private',
                        'is_verified', 'profile_pic_url', 'last_scanned_date'
                    ])
                    users_set.add(fetched_user_id)
                    user_id = fetched_user_id
                    logging.info(f"Fetched and updated user_id for {username}: {user_id}")
                except instaloader.exceptions.ProfileNotExistsException:
                    logging.error(f"No profile found for user ID {fetched_user_id}. The user may have blocked you.")
                    add_blocked_user(fetched_user_id)
                    continue
                except instaloader.exceptions.InstaloaderException as e:
                    logging.error(f"Instaloader exception while fetching profile for user_id {fetched_user_id}: {e}")
                    continue
                except Exception as e:
                    logging.error(f"Unexpected error while fetching profile for user_id {fetched_user_id}: {e}")
                    continue
            else:
                logging.error(f"Skipping user {username} due to missing user_id.")
                continue  # Skip to next user if user_id cannot be fetched

        # Check if user is blocked
        if user_id in blocked_users_set:
            logging.warning(f"User ID {user_id} is in {BLOCKED_USERS_CSV}. Skipping.")
            continue

        # Check if scan is required
        if is_scan_required(last_scanned_str, cutoff_date):
            logging.info(f"Scan required for user: {username}")

            # Fetch user profile
            profile = fetch_profile(loader, user_id)
            if not profile:
                logging.error(f"Skipping user {username} due to failed profile fetch.")
                continue  # Skip to next user if profile fetching failed

            # Process all posts of the user
            process_posts(
                loader, profile, user_id,
                posts_set, POSTS_CSV,
                likes_set, LIKES_CSV,
                comments_set, COMMENTS_CSV,
                users_set, USERS_CSV
            )

            # Update last scanned date to current date
            current_date = datetime.now().strftime(DATE_FORMAT)
            update_last_scanned(USERS_CSV, username, current_date)
        else:
            logging.info(f"No scan needed for user: {username}.")

    logging.info("\nData fetching and CSV updating completed.")

if __name__ == "__main__":
    main()
