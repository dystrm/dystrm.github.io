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
        log(f"[X] 트윗 전송 완료 ✅\nhttps://x.com/i/web/status/{response.data['id']}")
    except Exception as e:
        error_msg = f"[X] 트윗 전송 실패 ❌: {e}"
        log(error_msg)

        # ✅ 디스코드로 전체 트윗 내용 + 오류 메시지 전송
        full_msg = f"❌ 트윗 전송 실패!\n사유: {e}\n\n📢 트윗 내용:\n{text}"
        send_discord_alert(full_msg)
