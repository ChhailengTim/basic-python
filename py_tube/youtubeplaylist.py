import yt_dlp

url = input("🎥 Paste YouTube/Playlist link here: ")

ydl_opts = {
    # Force QuickTime-friendly codecs
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
    "merge_output_format": "mp4", 

    # Save in playlist folder with numbering
    "outtmpl": "%(playlist_title)s/%(playlist_index)03d - %(title).100s.%(ext)s",

    # General settings
    "noplaylist": False,         # allow full playlist downloads
    "ignoreerrors": True,        # skip unavailable videos
    "progress_hooks": [lambda d: print(f"▶️ {d['status']}: {d.get('filename', '')}")],

    # Post-processing (re-encode if necessary for QuickTime)
    "postprocessors": [
        {
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"  # re-encode if needed
        }
    ]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
