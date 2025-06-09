from playwright.sync_api import sync_playwright
from config import TITLE, ARTIST
from utils import log, save_chart, normalize_text

def get_vibe_top100():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,  # 👈 처음엔 headless=False로 확인
                args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"]
            )

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="ko-KR",
                viewport={"width": 1280, "height": 800},
                java_script_enabled=True
            )

            page = context.new_page()
            page.goto("https://vibe.naver.com/chart/total", timeout=60000)
            page.wait_for_timeout(5000)

            # 구독 팝업 닫기
            try:
                page.locator("a[role=button] >> text=팝업 닫기").click(timeout=3000)
                log("[VIBE] 구독 팝업 닫음 ✅")
            except:
                log("[VIBE] 구독 팝업 없음 또는 닫기 실패 ❌")

            page.evaluate("""document.querySelector(".floating_bar")?.remove();""")
            page.wait_for_timeout(1000)

            for _ in range(5):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(500)

            # 더보기 클릭
            page.evaluate("""
                const btn = document.querySelector(".btn_more_list a.link");
                if (btn) {
                    btn.scrollIntoView({ behavior: "smooth", block: "center" });
                    setTimeout(() => btn.click(), 300);
                }
            """)
            page.wait_for_timeout(5000)

            # 직접 Playwright DOM 접근 (BeautifulSoup 제거)
            rows = page.locator("div.tracklist table tbody tr")
            count = rows.count()

            if count < 100:
                log(f"[VIBE] 로딩된 곡 수 부족: {count}곡 ⚠️")
            else:
                log(f"[VIBE] {count}곡 로딩 완료 ✅")

            target_title = normalize_text(TITLE)
            target_artist = normalize_text(ARTIST)

            for i in range(count):
                try:
                    row = rows.nth(i)
                    rank = row.locator("td.rank span.text").inner_text().strip()
                    title = row.locator("td.song .link_text span").inner_text().strip()
                    artist = row.locator("td.song .artist_sub").get_attribute("title") or ""

                    if normalize_text(title) == target_title and normalize_text(artist) == target_artist:
                        log(f"[VIBE] '{TITLE}' 현재 순위: {rank}")
                        save_chart("vibe", int(rank))
                        return
                except:
                    continue

            log(f"[VIBE] '{TITLE}' 순위 없음")
            save_chart("vibe", None)

            browser.close()

    except Exception as e:
        log(f"[VIBE] 크롤링 실패 ❌: {e}")
        save_chart("vibe", None)

# if __name__ == "__main__":
#     get_vibe_top100()