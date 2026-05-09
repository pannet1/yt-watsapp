import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

YOUTUBE_COOKIES_FILE = os.getenv("YOUTUBE_COOKIES_FILE", "cookies.txt")
WHATSAPP_PHONE_NUMBER = os.getenv("WHATSAPP_PHONE_NUMBER", "")
MAX_VIDEOS_TO_DOWNLOAD = int(os.getenv("MAX_VIDEOS_TO_DOWNLOAD", "5"))
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "downloads")

OUTPUT_DIR.mkdir(exist_ok=True)