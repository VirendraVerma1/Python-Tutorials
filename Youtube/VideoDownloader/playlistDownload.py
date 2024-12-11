import yt_dlp

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['filename']} - {d['_percent_str']} at {d['_speed_str']}")
    elif d['status'] == 'finished':
        print(f"Finished downloading {d['filename']}")

def download_playlist(playlist_url):
    ydl_opts = {
        'outtmpl': 'playlist_downloads/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

if __name__ == "__main__":
    playlist_url = 'https://www.youtube.com/playlist?list=PLBCF2DAC6FFB574DE'
    download_playlist(playlist_url)
