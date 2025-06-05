import tweepy
from config import TWITTER_API
from utils import log, send_discord_alert

def post_to_x(text):
    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API["consumer_key"],
            consumer_secret=TWITTER_API["consumer_secret"],
            access_token=TWITTER_API["access_token"],
            access_token_secret=TWITTER_API["access_token_secret"]
        )
        response = client.create_tweet(text=text)
        tweet_url = f"https://x.com/i/web/status/{response.data['id']}"
        log(f"[X] 트윗 전송 완료 ✅\n{tweet_url}")
        #send_discord_alert(f"✅ 트윗 전송 완료!\n{tweet_url}")

    except tweepy.errors.TooManyRequests as e:
        reset_time = e.response.headers.get("x-rate-limit-reset")
        if reset_time:
            from datetime import datetime
            reset_dt = datetime.fromtimestamp(int(reset_time))
            log(f"[X] 트윗 전송 실패 ❌: Rate Limit 초과. {reset_dt} 에 재시도 가능.")
            send_discord_alert(f"❌ 트윗 전송 실패: Rate Limit 초과.\n⏳ 재시도 가능 시각: {reset_dt}\n\n📢 트윗 내용:\n{text}")
        else:
            log(f"[X] 트윗 전송 실패 ❌: TooManyRequests (헤더 없음)")
            send_discord_alert(f"❌ 트윗 전송 실패: TooManyRequests\n📢 트윗 내용:\n{text}")

    except Exception as e:
        error_msg = f"[X] 트윗 전송 실패 ❌: {e}"
        log(error_msg)
        full_msg = f"❌ 트윗 전송 실패!\n사유: {e}\n\n📢 트윗 내용:\n{text}"
        send_discord_alert(full_msg)