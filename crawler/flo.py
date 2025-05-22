from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart
import time

def get_flo_top100():
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        url = "https://www.music-flo.com/browse?chartId=1"
        driver.get(url)
        time.sleep(2)
        for _ in range(3):
            try:
                more_btn = driver.find_element(By.CLASS_NAME, "btn_list_more")
                if more_btn.is_displayed():
                    driver.execute_script("arguments[0].click();", more_btn)
                    time.sleep(2)
            except:
                break
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        rows = soup.select("table.track_list_table tbody tr")
        for row in rows:
            try:
                rank = row.select_one("td.num").text.strip()
                title = row.select_one("td.info .tit__text").text.strip().lower()
                artist = row.select_one("td.artist").text.strip().lower()
                if TITLE.lower() in title and ARTIST.lower() in artist:
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