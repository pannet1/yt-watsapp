# YouTube Shorts to WhatsApp Status

## Setup

### 1. YouTube Cookies
To fetch liked videos, you need to export your YouTube cookies:

1. Install "Get cookies.txt LOCALLY" extension in Chrome
2. Go to youtube.com and log in
3. Click the extension and export cookies for youtube.com
4. Save as `cookies.txt` in this project folder

### 2. WhatsApp Configuration
Set your phone number in `.env`:
```
WHATSAPP_PHONE_NUMBER=+1234567890
```

Note: pywhatkit sends videos as messages. For status, manually add after receiving.

## Usage

```bash
cd /home/pannet1/programs/python/github.com/pannet1/yt-watsapp
source .venv/bin/activate
python main.py
```

## How It Works
1. Fetches liked videos from YouTube (requires cookies)
2. Filters for Shorts (videos with /shorts/ in URL or ≤60s)
3. Downloads up to MAX_VIDEOS_TO_DOWNLOAD videos
4. Sends videos to WhatsApp contact via pywhatkit

## Notes
- WhatsApp status updates require WhatsApp Business API
- This script sends videos as messages - add to status manually
- Videos are saved in `downloads/` folder