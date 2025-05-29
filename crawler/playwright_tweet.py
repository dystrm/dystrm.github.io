from playwright.sync_api import sync_playwright
import time

def tweet_with_playwright(tweet_text: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="twitter_session.json")
        page = context.new_page()

        # 트위터 글쓰기 페이지 접속
        page.goto("https://twitter.com/compose/tweet", timeout=60000)

        # 트윗 입력
        time.sleep(2)
        page.keyboard.insert_text(tweet_text)
        time.sleep(1)

        # 작성 버튼 클릭
        try:
            page.locator('button[data-testid="tweetButton"]').click()
            print("[Playwright] 트윗 전송 완료 ✅")
        except Exception as e:
            print(f"[Playwright] 트윗 전송 실패 ❌: {e}")

        time.sleep(2)
        context.storage_state(path="twitter_session.json")
        context.close()
        browser.close()


# from playwright.sync_api import sync_playwright
# import time

# def tweet_with_playwright(tweet_text):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(storage_state="twitter_session.json")
#         page = context.new_page()

#         page.goto("https://twitter.com/compose/tweet")
#         time.sleep(3)

#         # 트윗 입력
#         page.keyboard.type(tweet_text)
#         time.sleep(1)

#         # 트윗 버튼 클릭
#         page.locator('button[data-testid="tweetButton"]').click()
#         time.sleep(2)

#         print("✅ 트윗 전송 완료 (Playwright)")
#         browser.close()