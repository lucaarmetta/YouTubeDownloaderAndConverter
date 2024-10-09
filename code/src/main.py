import yt_dlp
import os

def convert_youtube_url_to_mp3(youtube_url: str, destination: str, ffmpeg_path: str = None, codec: str = 'mp3', quality: str = '256') -> str | None:
    """
    convert a YouTube video to an audio file in the specified format using yt-dlp and ffmpeg.
    :param youtube_url: URL of the YouTube video.
    :param destination: directory where the converted file will be saved. defaults to the /Downloads folder.
    :param ffmpeg_path: optional path to the ffmpeg binary. if None, it assumes ffmpeg is in the system PATH.
    :param codec: audio codec for the output file (default is 'mp3').
    :param quality: audio quality (default is '256').
    :return: path to the converted audio file.
    """
    # set default destination to /Downloads folder if not provided
    if destination is None:
        home = os.path.expanduser("~")  # get the user's home directory
        destination = os.path.join(home, "Downloads")  # append /Downloads
    # ensure destination directory exists
    if not os.path.exists(destination):
        os.makedirs(destination)
    # build options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': quality,
        }],
        'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
        'ffmpeg_location': ffmpeg_path or 'ffmpeg',  # use provided ffmpeg path or assume it's in PATH
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print(f"Download and conversion successful! File saved to: {destination}")
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video: {str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
    return destination

# example usage
if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=...'
    destination = None # optional: specify ffmpeg path or leave None
    ffmpeg_path = '/opt/homebrew/bin/ffmpeg'  # optional: specify ffmpeg path or leave None
    mp3_file_path = convert_youtube_url_to_mp3(youtube_url, destination, ffmpeg_path)