from playwright.sync_api import sync_playwright
import time
import sys

# ✅ 인자 확인
print("[DEBUG] argv:", sys.argv)

if len(sys.argv) < 2:
    print("❌ 트윗 메시지가 전달되지 않았습니다.")
    sys.exit(1)

tweet_text = sys.argv[1]
print("[DEBUG] 받은 트윗 내용 일부:", tweet_text[:50])  # 로그용

def tweet_with_playwright(tweet_text: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False: 디버깅 가능
        context = browser.new_context(storage_state="twitter_session.json")
        page = context.new_page()

        try:
            # ✅ 트윗 작성 페이지 접속
            print("[DEBUG] 트윗 페이지 이동 중...")
            page.goto("https://twitter.com/compose/tweet", timeout=60000)
            time.sleep(2)

            # ✅ 트윗 입력
            print("[DEBUG] 트윗 입력 중...")
            page.keyboard.insert_text(tweet_text)
            time.sleep(1)

            # ✅ 트윗 버튼 클릭
            print("[DEBUG] 트윗 버튼 클릭 시도...")
            tweet_btn = page.locator('div[data-testid="tweetButtonInline"], button[data-testid="tweetButton"]')
            tweet_btn.click()
            time.sleep(3)

            # ✅ 성공 여부 체크
            textarea = page.locator('div[aria-label="트윗 텍스트"]')
            if textarea.is_visible() and textarea.inner_text().strip() != "":
                print("❌ 트윗 전송 실패: 입력란이 그대로 남아 있음")
            else:
                print("✅ [Playwright] 트윗 전송 성공")

        except Exception as e:
            print(f"❌ [Playwright] 트윗 전송 중 오류 발생: {e}")

        finally:
            # ✅ 세션 저장 및 종료
            context.storage_state(path="twitter_session.json")
            context.close()
            browser.close()

# ✅ 실행
tweet_with_playwright(tweet_text)
