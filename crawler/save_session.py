from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False로 브라우저 띄우기
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twitter.com/login")

    input("🟢 트위터에 로그인한 뒤, 콘솔에 Enter를 눌러주세요...")

    # ✅ 로그인 세션 저장
    context.storage_state(path="twitter_session.json")
    print("✅ 세션 저장 완료")

    browser.close()
