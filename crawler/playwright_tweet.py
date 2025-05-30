from playwright.sync_api import sync_playwright, TimeoutError
import time

def tweet_with_playwright(tweet_text: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="twitter_session.json")
        page = context.new_page()

        # 트윗 작성 페이지 열기
        page.goto("https://twitter.com/compose/tweet", timeout=60000)
        time.sleep(2)

        # 트윗 입력
        page.keyboard.insert_text(tweet_text)
        time.sleep(1)

        try:
            # 트윗 버튼 클릭
            tweet_btn = page.locator('div[data-testid="tweetButtonInline"], button[data-testid="tweetButton"]')
            tweet_btn.click()
            time.sleep(3)

            # 성공 여부 체크 (작성란이 비워졌는지 확인)
            textarea = page.locator('div[aria-label="트윗 텍스트"]')
            if textarea.is_visible() and textarea.inner_text().strip() != "":
                print("❌ 트윗 전송 실패: 입력란이 그대로 남아 있음")
            else:
                print("✅ [Playwright] 트윗 전송 성공")

        except Exception as e:
            print(f"❌ [Playwright] 트윗 전송 중 오류: {e}")

        # 세션 저장 및 종료
        context.storage_state(path="twitter_session.json")
        context.close()
        browser.close()
