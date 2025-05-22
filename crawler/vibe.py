from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart
import time

def get_vibe_top100():
    try:
        url = "https://vibe.naver.com/chart/total"
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        rows = soup.select("div.tracklist table tbody tr")
        for row in rows:
            rank_tag = row.select_one("td.rank span.text")
            title_tag = row.select_one("td.song .link_text span")
            artist_tag = row.select_one("td.song .artist_sub")
            rank = rank_tag.text.strip() if rank_tag else ""
            title = title_tag.text.strip().lower() if title_tag else ""
            artist = artist_tag["title"].strip().lower() if artist_tag and artist_tag.has_attr("title") else ""
            if TITLE.lower() in title and ARTIST.lower() in artist:
                log(f"[VIBE] '{TITLE}' 현재 순위: {rank}")
                save_chart("vibe", int(rank))
                return
        log(f"[VIBE] '{TITLE}' 순위 없음")
        save_chart("vibe", None)
    except Exception as e:
        log(f"[VIBE] 크롤링 실패 ❌: {e}")
        save_chart("vibe", None)