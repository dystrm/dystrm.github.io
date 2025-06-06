from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart

def get_vibe_top100():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = browser.new_page()
            page.goto("https://vibe.naver.com/chart/total")
            page.wait_for_timeout(3000)

            # 구독 팝업 닫기
            try:
                page.locator("a[role=button] >> text=팝업 닫기").click(timeout=3000)
                log("[VIBE] 구독 팝업 닫음 ✅")
            except:
                log("[VIBE] 구독 팝업 없음 또는 닫기 실패 ❌")

            # 방해 요소 제거
            page.evaluate("""document.querySelector(".floating_bar")?.remove();""")
            page.wait_for_timeout(500)

            # 스크롤 & 더보기 클릭
            for _ in range(5):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(400)

            page.evaluate("""
                const btn = document.querySelector(".btn_more_list a.link");
                if (btn) {
                    btn.scrollIntoView({ behavior: "smooth", block: "center" });
                    setTimeout(() => btn.click(), 300);
                }
            """)
            page.wait_for_timeout(4000)

            # 300곡 로딩 대기
            try:
                page.wait_for_function(
                    "() => document.querySelectorAll('div.tracklist table tbody tr').length >= 300",
                    timeout=10000
                )
                log("[VIBE] 300곡 로딩 완료 ✅")
            except:
                log("[VIBE] 300곡 로딩 실패 ⚠️")

            # 페이지 파싱
            soup = BeautifulSoup(page.content(), "html.parser")
            browser.close()

            rows = soup.select("div.tracklist table tbody tr")
            for row in rows:
                try:
                    rank = row.select_one("td.rank span.text").text.strip()
                    title = row.select_one("td.song .link_text span").text.strip().lower()
                    artist = row.select_one("td.song .artist_sub").get("title", "").strip().lower()

                    if TITLE.lower() in title and ARTIST.lower() in artist:
                        log(f"[VIBE] '{TITLE}' 현재 순위: {rank}")
                        save_chart("vibe", int(rank))  # 현재 시각 기준 저장
                        return
                except:
                    continue

            log(f"[VIBE] '{TITLE}' 순위 없음")
            save_chart("vibe", None)

    except Exception as e:
        log(f"[VIBE] 크롤링 실패 ❌: {e}")
        save_chart("vibe", None)
