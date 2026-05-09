import subprocess
from pathlib import Path

def send_to_whatsapp_status(video_path: Path, phone_number: str) -> bool:
    """
    Send video to WhatsApp status.
    
    Note: WhatsApp doesn't provide a public API for status updates.
    Options:
    1. WhatsApp Business API - requires business account
    2. Device automation (ADB/Tasker)
    3. Manual: Send video to yourself, then add to status
    
    This implementation attempts to send the video as a message using pywhatkit.
    """
    try:
        import pywhatkit
        
        pywhatkit.send_video(
            receiver_phone_number=phone_number,
            video_path=str(video_path),
            tab_close=True
        )
        return True
    except ImportError:
        print("pywhatkit not installed. Installing...")
        subprocess.run(['pip', 'install', 'pywhatkit'], check=True)
        return send_to_whatsapp_status(video_path, phone_number)
    except Exception as e:
        print(f"Failed to send video via WhatsApp: {e}")
        return False

def send_video_to_contact(video_path: Path, phone_number: str) -> bool:
    """
    Alternative: Send video as a message to a contact.
    After receiving, user can manually add to status.
    """
    try:
        import pywhatkit
        
        pywhatkit.send_video(
            receiver_phone_number=phone_number,
            video_path=str(video_path),
            tab_close=True
        )
        print(f"Video sent to {phone_number}. Add to status manually.")
        return True
    except Exception as e:
        print(f"Failed to send video: {e}")
        return False