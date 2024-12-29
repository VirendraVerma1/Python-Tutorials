import instaloader
from urllib.parse import urlparse

def get_post_info(post_url):
    # Initialize Instaloader
    L = instaloader.Instaloader()

    # Extract shortcode from URL
    parsed_url = urlparse(post_url)
    shortcode = parsed_url.path.split('/')[-2]  # URL format: https://www.instagram.com/p/SHORTCODE/

    try:
        # Load post using shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Extract desired information
        post_info = {
            'owner_username': post.owner_username,
            'caption': post.caption,
            'likes': post.likes,
            'comments': post.comments,
            'date': post.date,
            'url': post.url,
            'is_video': post.is_video,
            'hashtags': post.caption_hashtags,
            'mentions': post.caption_mentions,
        }

        return post_info

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    url = "https://www.instagram.com/p/DDQ28HmIkQo/"  # Replace with the actual post URL
    info = get_post_info(url)
    if info:
        for key, value in info.items():
            print(f"{key}: {value}")
