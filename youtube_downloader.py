import os
import concurrent.futures
from pytube import Playlist
import yt_dlp

def download_video(video_url, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Downloaded: {video_url}")
    except Exception as e:
        print(f"Error downloading {video_url}: {str(e)}")

def download_playlist(playlist_url, output_dir='music', max_workers=5):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the playlist
    playlist = Playlist(playlist_url)

    # Use ThreadPoolExecutor for concurrent downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit download tasks for each video in the playlist
        futures = [executor.submit(download_video, video_url, output_dir) for video_url in playlist.video_urls]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

    print("Download complete!")

if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/watch?v=Viu7NTafSfU&list=PLi5pWrniefABw_trT9vL32CvBW_PcEJd2&index=16&ab_channel=smoshycat"
    max_workers = 16
    download_playlist(playlist_url, max_workers=max_workers)