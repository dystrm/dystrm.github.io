from main_post import build_message
from playwright_tweet import tweet_with_playwright

def main():
    tweet = build_message()
    print("[DEBUG] 트윗 메시지:\n", tweet)
    tweet_with_playwright(tweet)

if __name__ == "__main__":
    main()