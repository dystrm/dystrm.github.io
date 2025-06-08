import json
import os

# 기본 정보
TITLE = "반딧불 (Little Light)"
ARTIST = "도영 (DOYOUNG)"
VIDEO_ID = "Hf2wjEU2rzo"
DATA_DIR = "../js/data"
DISCORD_ALERT_ENABLED = True

# 비밀 키 경로 설정
SECRETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../secrets"))

def load_json(filename):
    path = os.path.join(SECRETS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Twitter API 정보
TWITTER_API = load_json("twitter_secrets.json")

# Discord Webhook URL
DISCORD_WEBHOOK_URL = load_json("discord_secrets.json")["webhook_url"]
