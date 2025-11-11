import os
import requests
import time
from datetime import datetime
from config import CONFIG

class UltimateFacebookDownloader:
    def __init__(self):
        self.access_token = CONFIG['access_token']
        self.cookies = self._parse_cookies(CONFIG['cookies'])
        self.page_id = CONFIG['page_id']
        self.output_dir = CONFIG['output_dir']
        self.api_version = CONFIG['graph_api_version']
        self.photo_limit = CONFIG['photo_limit']
        self.max_photos = CONFIG['max_photos']
        self.retry_failed = CONFIG['retry_failed']
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.failed_downloads = []
        
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"⚡ Ultimate Facebook Downloader (API v{self.api_version})")

    def _parse_cookies(self, cookie_string):
        return dict(pair.split('=') for pair in cookie_string.split('; ')) if cookie_string else {}

    def _make_request(self, url, params=None):
        params = params or {}
        params['access_token'] = self.access_token
        
        try:
            response = requests.get(
                url,
                params=params,
                cookies=self.cookies,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️ Request failed: {str(e)[:100]}...")
            return None

    def _get_output_path(self, created_time):
        """Organize photos by year/month"""
        dt = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S%z')
        return os.path.join(
            self.output_dir,
            str(dt.year),
            f"{dt.month:02d}"
        )

    def get_all_photos(self):
        """Retrieve all photos with pagination"""
        url = f"{self.base_url}/{self.page_id}/photos"
        params = {
            'fields': 'id,created_time,images',
            'limit': self.photo_limit,
            'type': 'uploaded'
        }
        
        all_photos = []
        while url and len(all_photos) < self.max_photos:
            data = self._make_request(url, params)
            if not data or not data.get('data'):
                break
                
            all_photos.extend(data['data'])
            print(f"📥 Fetched {len(all_photos)} photos...", end='\r')
            url = data.get('paging', {}).get('next')
            time.sleep(0.5)  # Rate limiting
            
        return all_photos

    def download_photo(self, photo):
        """Download single photo in original quality"""
        photo_id = photo['id']
        created_time = photo['created_time']
        images = photo.get('images', [])
        
        if not images:
            return False
            
        original_url = images[0]['source']  # First image is always original
        output_dir = self._get_output_path(created_time)
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{photo_id}_{created_time[:10]}.jpg"
        filepath = os.path.join(output_dir, filename)
        
        try:
            # Skip if already downloaded
            if os.path.exists(filepath):
                print(f"⏩ Already exists: {filename}")
                return True
                
            with requests.get(original_url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            print(f"✅ Downloaded: {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed {filename}: {str(e)[:100]}...")
            self.failed_downloads.append(photo)
            return False

    def run(self):
        print("\n" + "="*50)
        print(f"Downloading ALL original photos from page: {self.page_id}")
        print(f"Saving to: {os.path.abspath(self.output_dir)}")
        print("="*50 + "\n")
        
        photos = self.get_all_photos()
        if not photos:
            print("🚨 No photos found or access denied")
            return
            
        print(f"\n🔥 Found {len(photos)} photos. Downloading...\n")
        
        success = 0
        for photo in photos:
            if self.download_photo(photo):
                success += 1
            time.sleep(0.3)  # Gentle on servers
            
        print(f"\n🎉 Successfully downloaded {success}/{len(photos)} photos")
        
        # Retry failed downloads if enabled
        if self.retry_failed and self.failed_downloads:
            print(f"\n🔄 Retrying {len(self.failed_downloads)} failed downloads...")
            retry_success = 0
            for photo in self.failed_downloads:
                if self.download_photo(photo):
                    retry_success += 1
                time.sleep(1)
            print(f"Recovered {retry_success} previously failed downloads")

if __name__ == "__main__":
    downloader = UltimateFacebookDownloader()
    downloader.run()