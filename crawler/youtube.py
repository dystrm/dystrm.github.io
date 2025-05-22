import requests
from config import VIDEO_ID

YOUTUBE_API_KEY = "AIzaSyBlutTPaSd_dQRXEHXfyKs-SkbGjYfaf-c"

def get_youtube_view_count():
    try:
        api_url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?part=statistics&id={VIDEO_ID}&key={YOUTUBE_API_KEY}"
        )
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        view_count = int(data["items"][0]["statistics"]["viewCount"])
        return view_count
    except Exception as e:
        print(f"[YouTube] API 오류: {e}")
        return 0
