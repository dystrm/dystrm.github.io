import tweepy
import time
import json
import os
from datetime import datetime

# 🔐 비밀 키 경로 설정
SECRETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../secrets"))

def load_json(filename):
    path = os.path.join(SECRETS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 🔐 test.json에서 Twitter API 정보 읽기
TWITTER_API = load_json("test.json")

# 1️⃣ X API v2 + OAuth 1.0a 인증
client = tweepy.Client(
    consumer_key=TWITTER_API["consumer_key"],
    consumer_secret=TWITTER_API["consumer_secret"],
    access_token=TWITTER_API["access_token"],
    access_token_secret=TWITTER_API["access_token_secret"]
)

# 2️⃣ 트윗
now = datetime.now()
text = f"🐦 자동 트윗 테스트 - {now.strftime('%Y-%m-%d %H:%M:%S')}"

try:
    client.create_tweet(text=text)
    print(f"✅ 트윗 성공: {text}")
except tweepy.TooManyRequests:
    print("⚠️ Rate limit 도달. 나중에 재시도")
except tweepy.TweepyException as e:
    print(f"❌ 트윗 실패: {e}")