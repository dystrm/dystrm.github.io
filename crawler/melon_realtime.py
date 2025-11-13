from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart, normalize_text
import time

def melon(chart_type="melon_realtime"):
    url = "https://m2.melon.com/cds/chart/android2/chartrealtime_list.htm"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-G973N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # ✅ JS 로딩 대기
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li .tit"))
        )
    except:
        log("⚠️ 멜론 페이지 로드 지연")

    time.sleep(1)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("li")

    target_title = normalize_text(TITLE)
    target_artist = normalize_text(ARTIST)

    found = False

    for row in rows:
        title_el = row.select_one("span.tit")
        artist_el = row.select_one("span.singer")
        rank_el = row.select_one("div[class^='rank']")  # rank3, rank4 등 포함

        if not (title_el and artist_el and rank_el):
            continue

        title = title_el.get_text(strip=True)
        artist = artist_el.get_text(strip=True)
        rank_text = rank_el.get_text(strip=True)

        # ✅ '01' → 1로 변환
        try:
            rank = int(rank_text.lstrip('0') or 0)
        except:
            continue

        if normalize_text(title) == target_title and normalize_text(artist) == target_artist:
            log(f"[MELON_REALTIME] '{TITLE}' 순위: {rank}")
            save_chart("melon_realtime", rank)
            found = True
            break

    if not found:
        log(f"[MELON_REALTIME] '{TITLE}' 순위 없음")
        save_chart("melon_realtime", None)


if __name__ == "__main__":
    melon()