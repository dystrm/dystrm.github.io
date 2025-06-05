from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from config import ARTIST
from utils import log
import datetime
import json
import os
import time
import re

def save_award_chart(rank, title, percent, vote, desc, week=None, remain=None):
    data_dir = "../js/data"
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, "melon_award.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {
            "artist": ARTIST,
            "history": []
        }

    timestamp = datetime.datetime.now().isoformat()
    data["history"].append({
        "timestamp": timestamp,
        "rank": rank,
        "title": title,
        "percent": percent,
        "vote": vote,
        "desc": desc,
        "week": week,
        "remain": remain
    })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def melon_award():
    url = "https://www.melon.com/melonaward/weekAward.htm"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # ✅ 주차 처리
    try:
        month_tag = soup.select_one(".sec-title .num-term01")
        week_tag = soup.select_one(".sec-title .num-term02")
        month = re.sub(r"[^0-9]", "", month_tag.get_text(strip=True))
        week = re.sub(r"[^0-9]", "", week_tag.get_text(strip=True))
        week_label = f"{month}월 {week}주차"
    except:
        week_label = None

    # ✅ 남은 시간 처리: N일 N시간 형식으로
    try:
        remain_block = soup.select_one("dl.col-closing-time dd")
        remain_label = ""

        if remain_block:
            text = remain_block.get_text(separator=" ", strip=True)
            day_match = re.search(r"(\d+)일", text)
            hour_match = re.search(r"(\d+)시간", text)

            day = day_match.group(1) if day_match else None
            hour = hour_match.group(1) if hour_match else None

            if day and hour:
                remain_label = f"{day}일 {hour}시간"
            elif day:
                remain_label = f"{day}일"
            elif hour:
                remain_label = f"{hour}시간"
            else:
                remain_label = None
        else:
            remain_label = None

    except:
        remain_label = None

    items = soup.select("li[class^='d_li_cookie_']")
    found = False

    for li in items:
        artist_tag = li.select_one(".author")
        if not artist_tag:
            continue

        singer = artist_tag.text.strip()
        if ARTIST.lower() in singer.lower():
            title = li.select_one(".song-name").text.strip()
            percent = li.select_one(".count-vote .graph .txt").text.strip()

            vote_dd = li.select_one(".count-vote dd.txt")
            desc_tag = vote_dd.select_one(".info")
            if desc_tag:
                desc = desc_tag.text.strip()
                desc_tag.extract()
            else:
                desc = ""
            vote = vote_dd.text.strip()

            rank = None
            rank_tag = li.select_one(".rank-area .rank")
            if rank_tag and "class" in rank_tag.attrs:
                for cls in rank_tag["class"]:
                    if cls.startswith("n"):
                        try:
                            rank = int(cls[1:])
                            break
                        except:
                            pass

            log(f"[MELON_AWARD] '{ARTIST}' 순위: {rank}, {title}, {percent}, {vote}, {desc}, {week_label}, {remain_label}")
            save_award_chart(rank, title, percent, vote, desc, week_label, remain_label)
            found = True
            break

    if not found:
        log(f"[MELON_AWARD] '{ARTIST}' 후보 없음")
        save_award_chart(None, None, None, None, None, week_label, remain_label)

if __name__ == "__main__":
    melon_award()
