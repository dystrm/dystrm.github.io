from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart
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
    time.sleep(2)

    # ✅ "더보기" 버튼 반복 클릭
    for _ in range(3):
        try:
            more_btn = driver.find_element(By.CLASS_NAME, "btn_more1")
            if more_btn.is_displayed():
                driver.execute_script("arguments[0].click();", more_btn)
                time.sleep(1.5)
            else:
                break
        except:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    rows = soup.select("li")
    for row in rows:
        try:
            rank = int(row.select_one("div.rank").text.strip())
            title = row.select_one("span.tit").text.strip()
            artist = row.select_one("span.singer").text.strip()
            if TITLE.lower() in title.lower() and ARTIST.lower() in artist.lower():
                log(f"[MELON_REALTIME] '{TITLE}' 순위: {rank}")
                save_chart("melon_realtime", rank)
                return
        except:
            continue

    log(f"[MELON_REALTIME] '{TITLE}' 순위 없음")
    save_chart("melon_realtime", None)

if __name__ == "__main__":
    melon()