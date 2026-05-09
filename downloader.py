import yt_dlp
import requests
import logging
from pathlib import Path
from config import OUTPUT_DIR, YOUTUBE_COOKIES_FILE

# Suppress yt-dlp logging
yt_dlp_logger = logging.getLogger('yt_dlp')
yt_dlp_logger.setLevel(logging.CRITICAL)

def get_liked_shorts(shuffle: bool = True):
    cookies_path = Path(__file__).parent / YOUTUBE_COOKIES_FILE
    
    if not cookies_path.exists():
        print(f"Error: Cookies file not found at {cookies_path}")
        print("Please export your YouTube cookies (see README for instructions)")
        return []
    
    ydl_opts = {
        'cookiefile': str(cookies_path),
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True,
        'playlistend': 50,
        'extract_flat': True,  # Just get playlist info, not detailed video info
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            liked_info = ydl.extract_info('https://www.youtube.com/playlist?list=LL', download=False)
            
        # Debug: Print what we got
        print(f"liked_info: {liked_info}")
        if liked_info:
            print(f"Playlist title: {liked_info.get('title', 'Unknown')}")
            entries = liked_info.get('entries', [])
            print(f"Number of entries: {len(entries)}")
            if entries:
                print(f"First entry: {entries[0]}")
    except Exception as e:
        print(f"Error fetching liked videos: {e}")
        print("Your cookies might be expired. Re-export them from browser and try again.")
        return []
        
    shorts = []
    if liked_info and 'entries' in liked_info:
        for entry in liked_info.get('entries', []):
            if not entry:
                continue
            url = entry.get('url', '')
            duration = entry.get('duration', 0) or 0
            
            is_short = '/shorts/' in url or (duration > 0 and duration <= 60)
            
            if is_short:
                shorts.append({
                    'url': url,
                    'title': entry.get('title', 'Unknown'),
                    'duration': duration,
                    'id': entry.get('id', '')
                })
    
    return shorts

def download_video(url: str, output_dir: Path = OUTPUT_DIR) -> Path | None:
    import subprocess
    
    cookies_path = Path(__file__).parent / YOUTUBE_COOKIES_FILE
    output_template = str(output_dir / '%(title)s.%(ext)s')
    
    # Use the yt-dlp from the virtual environment using python -m yt_dlp
    python_path = Path(__file__).parent / '.venv' / 'bin' / 'python'
    
    # Try with extractor args to bypass format issues
    cmd = [
        str(python_path), '-m', 'yt_dlp',
        '--cookies', str(cookies_path),
        '-o', output_template,
        '--no-warnings',
        '--quiet',
        '--extractor-args', 'youtube:player_client=web',
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"Failed to download {url}: {result.stderr}")
            return None
        
        # Find the downloaded file
        for f in output_dir.glob('*'):
            if f.suffix in ['.mp4', '.mkv', '.webm', '.flv']:
                return f
        
        return None
    except subprocess.TimeoutExpired:
        print(f"Timeout downloading {url}")
        return None
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def unlike_video(video_id: str) -> bool:
    """Unlike a YouTube video using cookies."""
    cookies_path = Path(__file__).parent / YOUTUBE_COOKIES_FILE
    
    if not cookies_path.exists():
        print(f"Error: Cookies file not found at {cookies_path}")
        return False
    
    # Parse cookies from file
    cookies = {}
    try:
        with open(cookies_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    parts = line.split('\t')
                    if len(parts) >= 7:
                        cookies[parts[5]] = parts[6]
    except Exception as e:
        print(f"Failed to read cookies: {e}")
        return False
    
    url = "https://www.youtube.com/service_ajax?name=likeEndpoint"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-YouTube-Client-Name": "1",
        "X-YouTube-Client-Version": "2.20210622.10.03",
    }
    data = f"video_id={video_id}&command=unlike"
    
    try:
        response = requests.post(url, headers=headers, data=data, cookies=cookies, timeout=10)
        if response.status_code == 200:
            print(f"  Unliked video: {video_id}")
            return True
        else:
            print(f"  Failed to unlike {video_id}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"  Error unliking {video_id}: {e}")
        return False