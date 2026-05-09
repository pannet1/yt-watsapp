# YouTube Shorts to WhatsApp Status - Specification

## Project Overview
- **Project Name**: yt-watsapp
- **Type**: Automation script
- **Core Functionality**: Download YouTube Shorts from liked videos and send to WhatsApp status
- **Target User**: Personal use for sharing liked Shorts to WhatsApp status

## Architecture

### Components
1. **YouTube Liked Videos Fetcher**: Uses yt-dlp to fetch liked videos via YouTube API
2. **Shorts Filter**: Filters for Shorts (videos with `/shorts/` in URL or duration < 60s)
3. **Video Downloader**: Downloads video in suitable format for WhatsApp
4. **WhatsApp Status Sender**: Sends video to WhatsApp status using WhatsApp Business API or direct device transfer

### Key Files
- `main.py` - Main orchestrator script
- `config.py` - Configuration (YouTube cookies, WhatsApp settings)
- `downloader.py` - YouTube video downloading logic
- `whatsapp_sender.py` - WhatsApp status sending logic
- `.env` - Environment variables (API keys, credentials)

## Known Issues / Considerations
- YouTube requires authentication to fetch liked videos (cookie-based)
- WhatsApp API requires WhatsApp Business account or alternative methods
- Video format must be compatible with WhatsApp status (MP4, < 30s recommended)

## Dependencies
- yt-dlp (video downloading)
- python-dotenv (config management)
- pywhatkit or whatsapp-business-api (WhatsApp sending)

## Setup Requirements
1. YouTube cookies file (cookies.txt) for authentication
2. WhatsApp sending method (API or device-based)
3. Environment variables in .env file