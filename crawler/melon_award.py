from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from config import ARTIST
from utils import log
import datetime
import json
import os
import re

def save_award_chart(rank, title, percent, vote, desc, week=None, remain=None):
    import traceback

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.normpath(os.path.join(BASE_DIR, "../js/data"))
        os.makedirs(data_dir, exist_ok=True)
        path = os.path.join(data_dir, "melon_award.json")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print("[WARN] 기존 파일 로드 실패, 새로 생성함:", e)
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

        print("✅ 저장 완료:", path)

    except Exception as e:
        print("❌ [FATAL] JSON 저장 실패:", e)
        traceback.print_exc()


def parse_remain_label(remain_block):
    try:
        spans = remain_block.find_all("span")
        nums = []
        label = ""
        for span in spans:
            cls = span.get("class", [])
            text = span.get_text(strip=True)

            if "txt-day" in cls:
                label += "".join(nums) + "일 "
                nums = []
            elif "txt-clock" in cls and "시간" in span.text:
                label += "".join(nums) + "시간"
                break
            elif "txt-clock" in cls and "분" in span.text:
                # 옵션: 분까지 포함하고 싶으면 여기서 처리
                break
            elif "txt-clock" in cls and "초" in span.text:
                break
            elif "num-wrap" in cls:
                # num-wrap은 건너뛰고 내부 span 숫자만 읽도록 함
                continue
            elif any(c.startswith("num") for c in cls):
                nums.append(text)

        return label.strip()
    except Exception as e:
        print("[DEBUG] parse_remain_label error:", e)
        return None

def melon_award():
    url = "https://www.melon.com/melonaward/weekAward.htm"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # ✅ 주차 정보
    try:
        month_tag = soup.select_one(".sec-title .num-term01")
        week_tag = soup.select_one(".sec-title .num-term02")
        month = re.sub(r"[^0-9]", "", month_tag.get_text(strip=True))
        week = re.sub(r"[^0-9]", "", week_tag.get_text(strip=True))
        week_label = f"{month}월 {week}주차"
    except:
        week_label = None

    # ✅ 남은 시간 정보
    try:
        remain_block = soup.select_one("dl.col-closing-time dd")
        remain_label = parse_remain_label(remain_block) if remain_block else None
    except:
        remain_label = None

    # ✅ 아티스트 검색
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

            log(f"[MELON_AWARD] '{ARTIST}' 순위: {rank}, {title}, {percent}, {vote}, {desc}, {week_label}, {remain_label or '없음'}")
            save_award_chart(rank, title, percent, vote, desc, week_label, remain_label)
            found = True
            break

    if not found:
        log(f"[MELON_AWARD] '{ARTIST}' 후보 없음")
        save_award_chart(None, None, None, None, None, week_label, remain_label)

if __name__ == "__main__":
    melon_award()
