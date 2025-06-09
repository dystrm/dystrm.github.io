import os
import sys
from playwright.sync_api import sync_playwright
import time

def safe_print(text):
    try:
        print(text.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))
    except:
        print("(출력 생략 - 인코딩 문제 발생)")

if len(sys.argv) < 2:
    safe_print("❌ 트윗 파일 경로가 전달되지 않았습니다.")
    sys.exit(1)

file_path = sys.argv[1]
with open(file_path, "r", encoding="utf-8") as f:
    tweet_text = f.read()

safe_print(f"[DEBUG] 트윗 내용 미리보기:\n{tweet_text}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "../secrets/twitter_session.json")

def tweet_with_playwright(tweet_text: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=SESSION_PATH)
        page = context.new_page()

        try:
            page.goto("https://twitter.com/compose/tweet", timeout=60000)
            time.sleep(2)
            page.keyboard.insert_text(tweet_text)
            time.sleep(1)
            page.evaluate("""() => {
                const blockers = document.querySelectorAll('div[role="presentation"]');
                blockers.forEach(el => el.remove());
            }""")
            tweet_btn = page.locator('div[data-testid="tweetButtonInline"], button[data-testid="tweetButton"]')
            tweet_btn.click(force=True)
            time.sleep(3)

            textarea = page.locator('div[aria-label="트윗 텍스트"]')
            if textarea.is_visible() and textarea.inner_text().strip() != "":
                safe_print("❌ 트윗 전송 실패: 입력란이 그대로 남아 있음")
            else:
                safe_print("✅ 트윗 전송 성공")

        except Exception as e:
            safe_print(f"❌ 트윗 전송 중 오류 발생: {e}")

        finally:
            context.storage_state(path=SESSION_PATH)
            context.close()
            browser.close()

tweet_with_playwright(tweet_text)
