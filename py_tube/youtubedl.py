
import yt_dlp

url = input("🎥 Paste YouTube link here: ")

ydl_opts = {
    "format": "bestvideo+bestaudio/best",  # highest quality
    "merge_output_format": "mp4",          # save as mp4
    "outtmpl": "%(title).100s.%(ext)s",    # filename = video title
    "noplaylist": True                     # only download single video
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
