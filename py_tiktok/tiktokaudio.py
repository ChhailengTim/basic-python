import os
import requests
import time
import tempfile
import subprocess
import shutil

try:
    from moviepy.editor import VideoFileClip
    _HAS_MOVIEPY = True
except Exception:
    VideoFileClip = None
    _HAS_MOVIEPY = False

def get_profile_videos(username, max_videos=None):
    all_videos = []
    cursor = 0

    while True:
        url = f"https://www.tikwm.com/api/user/posts?unique_id={username}&count=50&cursor={cursor}"
        try:
            res = requests.get(url, timeout=10).json()
        except Exception as e:
            print(f"   ❌ Failed to fetch page: {e}")
            break

        if not res.get("data") or not res["data"].get("videos"):
            break

        videos = res["data"]["videos"]
        all_videos.extend(videos)
        print(f"  → Fetched {len(all_videos)} videos so far...")

        if max_videos and len(all_videos) >= max_videos:
            all_videos = all_videos[:max_videos]
            break
            
    return all_videos

def download_audio_from_video(url, outpath, retries=3):
    """Download video temporarily and extract audio as MP3, using moviepy if available or ffmpeg as a fallback."""
    attempt = 0
    while attempt < retries:
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_path = tmp_file.name
                print(f"   ⏬ Downloading temp video for audio extraction...")
                r = requests.get(url, stream=True, timeout=30)
                r.raise_for_status()

                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        tmp_file.write(chunk)

                tmp_file.flush()

            print("   🎧 Extracting audio...")
            if _HAS_MOVIEPY and VideoFileClip is not None:
                clip = VideoFileClip(tmp_path)
                clip.audio.write_audiofile(outpath, codec="mp3")
                clip.close()
            else:
                # Fallback to ffmpeg command-line (requires ffmpeg installed)
                if not shutil.which("ffmpeg"):
                    raise RuntimeError("ffmpeg not found and moviepy is unavailable")
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    tmp_path,
                    "-vn",
                    "-acodec",
                    "libmp3lame",
                    "-q:a",
                    "2",
                    outpath,
                ]
                proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if proc.returncode != 0:
                    raise RuntimeError(f"ffmpeg failed: {proc.stderr.strip()[:200]}")

            try:
                os.remove(tmp_path)
            except Exception:
                pass
        except Exception as e:
            print(f"   ❌ Error: {e}. Retrying...")
            attempt += 1
            time.sleep(2)
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    print(f"   ❌ Failed after {retries} attempts, skipping.")
    return False
    print(f"   ❌ Failed after {retries} attempts, skipping.")
    return False


if __name__ == "__main__":
    username = input("Enter TikTok username (without @): ").strip()
    max_vids = input("How many videos to download? (Enter 'all' for everything): ").strip()

    max_videos = None if max_vids.lower() == "all" else int(max_vids)

    SAVE_DIR = f"downloads_audio_{username}"
    os.makedirs(SAVE_DIR, exist_ok=True)

    print(f"\n[1] Getting videos for @{username}...")
    videos = get_profile_videos(username, max_videos)
    print(f"[2] Found {len(videos)} videos to process.")

    for i, v in enumerate(videos, start=1):
        video_id = v.get("video_id") or v.get("id")
        filepath = os.path.join(SAVE_DIR, f"{video_id}.mp3")

        if os.path.exists(filepath):
            print(f"[3] Skipping {i}/{len(videos)} → {video_id}.mp3 (already exists)")
            continue

        print(f"[3] Processing {i}/{len(videos)} → {video_id}.mp3")

        success = download_audio_from_video(v["play"], filepath)
        if not success:
            print(f"   ⚠️ Skipped {video_id}.mp3 due to repeated errors.")

    print("\n[4] ✅ Finished extracting all audios (.mp3)!")
