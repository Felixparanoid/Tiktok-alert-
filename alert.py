import requests
from bs4 import BeautifulSoup
import os

TIKTOK_PROFILE_URL = "https://www.tiktok.com/@xfiibii"
PUSHOVER_TOKEN = os.environ.get("PUSHOVER_TOKEN")
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")

def get_latest_video():
    response = requests.get(TIKTOK_PROFILE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        video_tags = soup.find_all('div', {'class': 'tiktok-1n8z9jg-DivItemContainer'})
        if video_tags:
            latest_video = video_tags[0]
            video_desc = latest_video.find('div', {'class': 'tiktok-1oszu61-DivContainer'}).text
            return video_desc
    return None

def send_notification(video_desc):
    message = f"Neues TikTok-Video: {video_desc}"
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": "TikTok Alert"
    })

if __name__ == "__main__":
    latest_video_desc = get_latest_video()
    if latest_video_desc:
        send_notification(latest_video_desc)
