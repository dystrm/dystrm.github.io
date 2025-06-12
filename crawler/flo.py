from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart, normalize_text
import time

def get_flo_top100():
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        url = "https://www.music-flo.com/browse?chartId=1"
        driver.get(url)

        # ✅ 차트 테이블 로딩 대기
        try:
            # mac 30s
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.track_list_table tbody tr"))
            )
        except:
            log("[FLO] 차트 로딩 실패 ❌")
            driver.quit()
            save_chart("flo", None)
            return

        # ✅ 더보기 버튼 1회 클릭
        try:
            more_btn = driver.find_element(By.CLASS_NAME, "btn_list_more")
            if more_btn.is_displayed():
                driver.execute_script("arguments[0].click();", more_btn)
                time.sleep(2)
        except:
            pass

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        rows = soup.select("table.track_list_table tbody tr")
        target_title = normalize_text(TITLE)
        target_artist = normalize_text(ARTIST)

        for row in rows:
            try:
                rank = row.select_one("td.num").text.strip()

                title_el = row.select_one("td.info strong.tit__text > a")
                title = title_el.text.strip() if title_el else ""

                artist_el = row.select_one("td.artist .artist__link > a")
                artist = artist_el.text.strip() if artist_el else ""

                if normalize_text(title) == target_title and normalize_text(artist) == target_artist:
                    log(f"[FLO] '{TITLE}' 현재 순위: {rank}")
                    save_chart("flo", int(rank))
                    return
            except:
                continue

        log(f"[FLO] '{TITLE}' 순위 없음")
        save_chart("flo", None)

    except Exception as e:
        log(f"[FLO] 크롤링 실패 ❌: {e}")
        save_chart("flo", None)

# if __name__ == "__main__":
#     get_flo_top100()