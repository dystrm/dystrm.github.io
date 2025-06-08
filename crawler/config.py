import json
import os

# 기본 정보
TITLE = "반딧불 (Little Light)"
ARTIST = "도영 (DOYOUNG)"
VIDEO_ID = "Hf2wjEU2rzo"
DATA_DIR = "../js/data"
DISCORD_ALERT_ENABLED = True

# 비밀 키 불러오기
SECRET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../secrets/secrets.json"))

def load_secrets():
    with open(SECRET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

secrets = load_secrets()

TWITTER_API = secrets["twitter"]
DISCORD_WEBHOOK_URL = secrets["discord"]["webhook_url"]
