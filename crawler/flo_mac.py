from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart, normalize_text
import time

def get_flo_top100():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
            page = browser.new_page()
            page.goto("https://www.music-flo.com/browse?chartId=1", timeout=60000)
            page.wait_for_timeout(5000)  # 첫 로딩 대기 (기본 5초)

            # ✅ 더보기 버튼 최대 3회 클릭 (총 100곡 로딩용)
            for _ in range(3):
                try:
                    more_btn = page.locator("button.btn_list_more")
                    if more_btn.is_visible():
                        more_btn.click()
                        page.wait_for_timeout(1500)
                    else:
                        break
                except:
                    break

            html = page.content()
            browser.close()

            soup = BeautifulSoup(html, "html.parser")
            rows = soup.select("table.track_list_table tbody tr")

            target_title = normalize_text(TITLE)
            target_artist = normalize_text(ARTIST)

            for row in rows:
                try:
                    rank = row.select_one("td.num").text.strip()

                    title_el = row.select_one("td.info strong.tit__text > a")
                    title = title_el.text.strip() if title_el else ""

                    artist_el = row.select_one("td.artist a")
                    artist = artist_el.text.strip() if artist_el else ""

                    if normalize_text(title) == target_title and normalize_text(artist) == target_artist:
                        log(f"[FLO] '{TITLE}' 현재 순위: {rank}")
                        save_chart("flo", int(rank))
                        return
                except Exception as e:
                    log(f"[FLO] row 파싱 실패: {e}")
                    continue

            log(f"[FLO] '{TITLE}' 순위 없음")
            save_chart("flo", None)

    except Exception as e:
        log(f"[FLO] 전체 크롤링 실패 ❌: {e}")
        save_chart("flo", None)

# if __name__ == "__main__":
#     get_flo_top100()