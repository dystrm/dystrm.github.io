import tweepy
import time
from datetime import datetime

# 1️⃣ X API v2 + OAuth 1.0a 인증
client = tweepy.Client(
    consumer_key="7nkIctDg79LoEfofczn2kwap0",
    consumer_secret="0ZxTqF66rbQl3FPK4RBFN8pefqfithxR3gfesc1hypf4Y8lZF6",
    access_token="1912801041646866432-yEgmev0zzut2JJ24TDYrZtyLE3SG97",
    access_token_secret="9acS1MaLczgRs9qtfGjmAWeMPmiBH06s9lmVcGCp6FOlo"
)

# 2️⃣ 자동 트윗 루프
while True:
    now = datetime.now()
    hour = now.hour

    # 새벽 2시~6시(=02:00~06:59) 시간대 제외
    if 2 <= hour < 7:
        print(f"🌙 {now.strftime('%H:%M')} - 새벽 시간이라 트윗 생략")
        time.sleep(3600)
        continue

    # 트윗 내용 (중복 방지를 위해 현재 시각 포함)
    text = f"🐦 자동 트윗 테스트 - {now.strftime('%Y-%m-%d %H:%M:%S')}"

    try:
        client.create_tweet(text=text)
        print(f"✅ [{now.strftime('%H:%M')}] 트윗 성공: {text}")
    except tweepy.TooManyRequests:
        print("⚠️ Rate limit 도달. 30분 대기 중...")
        time.sleep(900)
    except tweepy.TweepyException as e:
        print(f"❌ 트윗 실패: {e}")

    # 1시간 대기 (3600초)
    time.sleep(3600)
