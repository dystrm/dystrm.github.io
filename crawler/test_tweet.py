from playwright.sync_api import sync_playwright
import time

import json
import os

# 경로
SECRETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../secrets"))
CONFIG_PATH = os.path.join(SECRETS_DIR, "test_config.json")

# config.json 읽기
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

USER_DATA_DIR = config["USER_DATA_DIR"]
CHROME_PATH = config["CHROME_PATH"]

def tweet_with_profile(text: str):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            executable_path=CHROME_PATH,
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-web-security",
            ],
        )

        page = browser.new_page()
        page.goto("https://x.com/compose/tweet")
        page.wait_for_selector('div[role="textbox"]')
        time.sleep(0.8)

        # ✔ fill 대신 type으로 키보드 입력처럼
        page.type('div[role="textbox"]', text, delay=15)

        # ✔ 버튼 disabled 풀릴 때까지 기다림
        page.wait_for_selector('button[data-testid="tweetButton"]:not([disabled])')

        # ✔ 클릭
        page.click('button[data-testid="tweetButton"]')

        print("✅ 트윗 완료!")
        time.sleep(2)

        browser.close()


if __name__ == "__main__":
    TXT_PATH = os.path.abspath("tweet.txt")

    if not os.path.exists(TXT_PATH):
        print("❌ tweet.txt 파일이 존재하지 않습니다.")
        exit(1)

    with open(TXT_PATH, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("❌ tweet.txt 내용이 비어 있습니다.")
        exit(1)

    tweet_with_profile(text)
