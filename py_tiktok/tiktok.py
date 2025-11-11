import os
import requests
import time

def get_profile_videos(username, max_videos=None):
    """Fetch all videos for a profile, paginated."""
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

        if not res["data"].get("hasMore"):
            break

        cursor = res["data"]["cursor"]

    return all_videos

def download_video(url, filename, retries=3):
    """Download and save video with retries and timeout."""
    attempt = 0
    while attempt < retries:
        try:
            r = requests.get(url, stream=True, timeout=30)
            r.raise_for_status()

            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return True

        except requests.exceptions.Timeout:
            print(f"   ⚠️ Timeout on attempt {attempt+1}. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error on attempt {attempt+1}: {e}. Retrying...")
        attempt += 1
        time.sleep(2)  # small wait before retry

    print(f"   ❌ Failed after {retries} attempts, skipping.")
    return False

if __name__ == "__main__":
    username = input("Enter TikTok username (without @): ").strip()
    max_vids = input("How many videos to download? (Enter 'all' for everything): ").strip()

    max_videos = None if max_vids.lower() == "all" else int(max_vids)

    SAVE_DIR = f"downloads_{username}"
    os.makedirs(SAVE_DIR, exist_ok=True)

    print(f"\n[1] Getting videos for @{username}...")
    videos = get_profile_videos(username, max_videos)
    print(f"[2] Found {len(videos)} videos to download.")

    for i, v in enumerate(videos, start=1):
        video_id = v.get("video_id") or v.get("id")
        filename = f"{video_id}.mp4"
        filepath = os.path.join(SAVE_DIR, filename)

        if os.path.exists(filepath):
            print(f"[3] Skipping {i}/{len(videos)} → {filename} (already exists)")
            continue

        print(f"[3] Downloading {i}/{len(videos)} → {filename}")

        success = download_video(v["play"], filepath)
        if not success:
            print(f"   ⚠️ Skipped {filename} due to repeated download errors.")

    print("\n[4] ✅ Finished downloading all videos!")
