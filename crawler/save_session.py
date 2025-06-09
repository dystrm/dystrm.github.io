from playwright.sync_api import sync_playwright
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 경로 (crawler/)
SESSION_PATH = os.path.join(BASE_DIR, "../secrets/twitter_session.json")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twitter.com/login")

    input("🟢 트위터에 로그인한 뒤, 콘솔에 Enter를 눌러주세요...")

    # ✅ 로그인 세션 저장
    context.storage_state(path=SESSION_PATH)
    print("✅ 세션 저장 완료")

    browser.close()
