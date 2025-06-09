import requests
from bs4 import BeautifulSoup
from config import TITLE, ARTIST
from utils import log, save_chart, normalize_text  # ✅ 추가

def get_genie_top200():
    try:
        headers = { "User-Agent": "Mozilla/5.0" }

        # ✅ 정규화된 기준값 준비
        target_title = normalize_text(TITLE)
        target_artist = normalize_text(ARTIST)

        for pg in range(1, 5):
            url = f"https://www.genie.co.kr/chart/top200?pg={pg}"
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            rows = soup.select("table.list-wrap tbody tr")

            for row in rows:
                try:
                    rank = row.select_one("td.number").text.split()[0].strip()
                    title = row.select_one("td.info a.title.ellipsis").text.strip()
                    artist = row.select_one("td.info a.artist.ellipsis").text.strip()

                    # ✅ normalize_text로 정확 비교
                    if normalize_text(title) == target_title and normalize_text(artist) == target_artist:
                        log(f"[GENIE] '{TITLE}' 현재 순위: {rank}")
                        save_chart("genie", int(rank))
                        return
                except:
                    continue

        log(f"[GENIE] '{TITLE}' 순위 없음")
        save_chart("genie", None)

    except Exception as e:
        log(f"[GENIE] 크롤링 실패 ❌: {e}")
        save_chart("genie", None)
