import sys
import tweepy
import time
import json
import os
from datetime import datetime

SECRETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../secrets"))

def load_json(filename):
    path = os.path.join(SECRETS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

TWITTER_API = load_json("test.json")

client = tweepy.Client(
    consumer_key=TWITTER_API["consumer_key"],
    consumer_secret=TWITTER_API["consumer_secret"],
    access_token=TWITTER_API["access_token"],
    access_token_secret=TWITTER_API["access_token_secret"]
)

if __name__ == "__main__":
    tweet_text = sys.argv[1]
    try:
        client.create_tweet(text=tweet_text)
        print("트윗 전송 성공")
    except Exception as e:
        print("트윗 실패:", e)

def post_to_x(text: str):
    try:
        client.create_tweet(text=text)
        print("트윗 전송 성공 (post_to_x)")
    except Exception as e:
        print("트윗 실패 (post_to_x):", e)
