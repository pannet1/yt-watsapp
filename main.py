import random
from config import WHATSAPP_PHONE_NUMBER, OUTPUT_DIR
from downloader import get_liked_shorts, download_video, unlike_video
from whatsapp_sender import send_video_to_contact

def main():
    print("Fetching liked Shorts from YouTube...")
    shorts = get_liked_shorts()
    
    if not shorts:
        print("No Shorts found in liked videos.")
        return
    
    print(f"Found {len(shorts)} Shorts")
    
    # Shuffle to get random videos
    random.shuffle(shorts)
    
    # Try up to 5 random videos max, stop on first success
    max_attempts = min(5, len(shorts))
    downloaded = None
    
    for i in range(max_attempts):
        short = shorts[i]
        print(f"Downloading {i+1}/{max_attempts}: {short['title']}")
        
        video_path = download_video(short['url'])
        if video_path and video_path.exists():
            downloaded = video_path
            print(f"  Saved: {video_path.name}")
            # Unlike the video so it won't be picked again
            unlike_video(short['id'])
            break  # Stop on successful download
    
    if downloaded is None:
        print(f"Failed all {max_attempts} attempts. Giving up.")
        return
    
    print(f"\nDownloaded: {downloaded.name}")
    
    if not WHATSAPP_PHONE_NUMBER:
        print("WHATSAPP_PHONE_NUMBER not set. Skipping WhatsApp send.")
        print(f"Videos saved to: {OUTPUT_DIR}")
        return
    
    print(f"Sending {downloaded.name} to WhatsApp...")
    if send_video_to_contact(downloaded, WHATSAPP_PHONE_NUMBER):
        print("  Sent successfully")
    else:
        print("  Failed to send")
    
    print("\nDone!")

if __name__ == "__main__":
    main()