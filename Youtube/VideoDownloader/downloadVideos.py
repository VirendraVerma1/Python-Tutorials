import yt_dlp

def download_video(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=9bZkp7q19f0'
    download_video(video_url)
