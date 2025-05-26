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
        
        # ✅ 디스코드에 성공 메시지 전송
        send_discord_alert(f"✅ 트윗 전송 완료!\n{tweet_url}")

    except Exception as e:
        error_msg = f"[X] 트윗 전송 실패 ❌: {e}"
        log(error_msg)
        full_msg = f"❌ 트윗 전송 실패!\n사유: {e}\n\n📢 트윗 내용:\n{text}"
        send_discord_alert(full_msg)
