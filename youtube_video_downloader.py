import os
import tqdm

from pytube import YouTube, Playlist


class YouTubeDownloader:
    """
    A class to download YouTube videos using pytube library.
    """

    def __init__(self, path=None):
        self.output_path = path
        os.makedirs(self.output_path, exist_ok=True)
        self.video = None

    def download_video(self, url):
        """
        Download the YouTube video with the highest available resolution.

        Parameters:
        - url (str): The URL of the YouTube video to download.
        """
        try:
            self.video = YouTube(url)
            stream = self.video.streams.get_highest_resolution()
            stream.download(output_path=self.output_path)
            print("Video downloaded successfully!")
        except Exception as e:
            print("An error occurred while downloading the video:", str(e))

    def download_playlist(self, playlist_url):
        """
        Download all videos in a YouTube playlist with the highest available resolution.

        Parameters:
        - playlist_url (str): The URL of the YouTube playlist to download.
        """
        try:
            playlist = Playlist(playlist_url)
            num_videos = len(playlist.video_urls)
            with tqdm.tqdm(total=num_videos, unit="video") as progress_bar:
                for video_link in playlist.video_urls:
                    self.download_video(video_link)
                    progress_bar.update(1)
            print("Playlist downloaded successfully!")
        except Exception as e:
            print("An error occurred while downloading the playlist:", str(e))


if __name__ == '__main__':
    downloader = YouTubeDownloader('output')
    choice = input("Enter '1' to download a video, '2' to download a playlist: ")

    if choice == "1":
        video_url = "Enter the YouTube video URL: "
        downloader.download_video(video_url)
    elif choice == "2":
        playlist_link = "Enter the YouTube video Playlist URL: "
        downloader.download_playlist(playlist_link)
    else:
        print("Invalid choice.")
