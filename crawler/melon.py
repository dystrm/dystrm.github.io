from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart
import time

def melon(chart_type):
    url_map = {
        "melon_top": "https://www.melon.com/chart/index.htm",
        "melon_hot": "https://www.melon.com/chart/hot100/index.htm"
    }

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.get(url_map[chart_type])
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    rows = soup.select("tr.lst50, tr.lst100")
    for row in rows:
        try:
            rank = int(row.select_one("span.rank").text.strip())
            title = row.select_one("div.ellipsis.rank01 > span > a").text.strip()
            artist = row.select_one("div.ellipsis.rank02 > a").text.strip()
            if TITLE.lower() in title.lower() and ARTIST.lower() in artist.lower():
                log(f"[{chart_type.upper()}] '{TITLE}' 순위: {rank}")
                save_chart(chart_type, rank)
                return
        except:
            continue

    log(f"[{chart_type.upper()}] '{TITLE}' 순위 없음")
    save_chart(chart_type, None)