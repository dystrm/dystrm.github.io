import tweepy

client = tweepy.Client(
    consumer_key="7nkIctDg79LoEfofczn2kwap0",
    consumer_secret="0ZxTqF66rbQl3FPK4RBFN8pefqfithxR3gfesc1hypf4Y8lZF6",
    access_token="1912801041646866432-yEgmev0zzut2JJ24TDYrZtyLE3SG97",           # Access Token
    access_token_secret="9acS1MaLczgRs9qtfGjmAWeMPmiBH06s9lmVcGCp6FOlo"  # Access Token Secret
)

client.create_tweet(text="🐦 API v2 + OAuth 1.0a 테스트 트윗!")
print("✅ 트윗 성공")
