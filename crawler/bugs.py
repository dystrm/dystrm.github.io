import requests
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart, normalize_text

def get_bugs_top100():
    try:
        url = "https://music.bugs.co.kr/chart/track/realtime/total"  # ✅ 최신 URL
        headers = { "User-Agent": "Mozilla/5.0" }
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table.list.trackList.byChart > tbody > tr")

        target_title = normalize_text(TITLE)
        target_artist = normalize_text(ARTIST)

        for row in rows:
            title_el = row.select_one("p.title > a")
            artist_el = row.select_one("p.artist > a")
            rank_el = row.select_one("div.ranking > strong")
            if not title_el or not artist_el or not rank_el:
                continue

            title = title_el.text.strip()
            artist = artist_el.text.strip()
            rank = rank_el.text.strip()

            if normalize_text(title) == target_title and normalize_text(artist) == target_artist:
                log(f"[BUGS] '{TITLE}' 현재 TOP100 순위: {rank}")
                save_chart("bugs", int(rank))
                return

        log(f"[BUGS] '{TITLE}' 순위 없음")
        save_chart("bugs", None)

    except Exception as e:
        log(f"[BUGS] 크롤링 오류: {e}")
        save_chart("bugs", None)
