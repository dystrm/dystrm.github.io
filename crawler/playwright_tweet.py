import os
import sys
from playwright.sync_api import sync_playwright
import time

def safe_print(text):
    try:
        print(text.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding))
    except:
        print("(출력 생략 - 인코딩 문제 발생)")

# 트윗 파일 경로 확인
if len(sys.argv) < 2:
    safe_print("❌ 트윗 파일 경로가 전달되지 않았습니다.")
    sys.exit(1)

file_path = sys.argv[1]
with open(file_path, "r", encoding="utf-8") as f:
    tweet_text = f.read().strip()[:280]

safe_print(f"[DEBUG] 트윗 내용 미리보기:\n{tweet_text}")

# 세션 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "../secrets/twitter_session.json")

def tweet_with_playwright(tweet_text: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # ✅ 자동 실행용: headless=True
        context = browser.new_context(storage_state=SESSION_PATH)
        page = context.new_page()

        try:
            page.goto("https://twitter.com/compose/tweet", timeout=60000)
            page.wait_for_selector('div[data-testid="tweetTextarea_0"]', timeout=10000)

            # 자동완성 및 오버레이 제거
            page.evaluate("""() => {
                document.querySelectorAll('[id^="typeaheadDropdown"]').forEach(el => el.remove());
                const blockers = Array.from(document.querySelectorAll('div')).filter(el => {
                    const style = window.getComputedStyle(el);
                    return style.pointerEvents !== 'none' && parseInt(style.zIndex) > 1000;
                });
                blockers.forEach(el => el.style.pointerEvents = 'none');
            }""")

            # ✅ 줄 단위 입력
            lines = tweet_text.split("\n")
            for line in lines:
                page.evaluate(f"""
                    () => {{
                        const el = document.querySelector('div[data-testid="tweetTextarea_0"]');
                        el.focus();
                        document.execCommand('insertText', false, `{line}`);
                    }}
                """)
                page.keyboard.press("Enter")
                time.sleep(0.05)

            # 트윗 버튼 활성화 대기
            tweet_btn = page.locator('button[data-testid="tweetButton"]')
            tweet_btn.wait_for(state="attached", timeout=3000)

            for _ in range(10):
                disabled = tweet_btn.get_attribute("disabled")
                aria_disabled = tweet_btn.get_attribute("aria-disabled")
                if disabled is None and aria_disabled != "true":
                    break
                time.sleep(0.2)
            else:
                raise Exception("❌ 버튼이 비활성 상태입니다.")

            # ✅ 트윗 버튼 클릭
            safe_print("🔘 트윗 버튼 클릭 시도 중...")
            tweet_btn.click(force=True)
            safe_print("✅ 트윗 버튼 클릭 완료")

        except Exception as e:
            safe_print(f"❌ 트윗 전송 중 오류 발생: {e}")

        finally:
            context.storage_state(path=SESSION_PATH)
            context.close()# ✅ 자동 종료 ON
            browser.close()# ✅ 자동 종료 ON

tweet_with_playwright(tweet_text)
