from melon import melon
from genie import get_genie_top200
from bugs import get_bugs_top100
from flo import get_flo_top100
from melon_realtime import melon as melon_realtime
from melon_award import melon_award
from vibe import get_vibe_top100
from utils import send_discord_alert
import os
import json
from datetime import datetime

def safe_run(name, func):
    try:
        func()
    except Exception as e:
        print(f"❌ {name} 크롤링 실패: {e}")
        send_discord_alert(f"{name} 크롤링 실패 ❌\n{e}")

def check_and_run_vibe():
    try:
        path = os.path.join("../js/data", "vibe.json")
        if not os.path.exists(path):
            safe_run("바이브", get_vibe_top100)
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        today = datetime.now().date().isoformat()
        today_entries = [d for d in data.get("history", []) if d["timestamp"].startswith(today)]

        if not today_entries:
            safe_run("바이브", get_vibe_top100)
        else:
            print("✅ 오늘자 바이브 데이터 이미 존재. 실행 생략")
    except Exception as e:
        send_discord_alert(f"바이브 확인/크롤링 중 오류 발생 ❌\n{e}")

def run_hourly():
    safe_run("멜론 Top", lambda: melon("melon_top"))
    safe_run("멜론 Hot", lambda: melon("melon_hot"))
    safe_run("멜론 실시간", melon_realtime)
    safe_run("지니", get_genie_top200)
    safe_run("벅스", get_bugs_top100)
    safe_run("플로", get_flo_top100)
    safe_run("멜론 어워드", melon_award)
    check_and_run_vibe()

if __name__ == "__main__":
    run_hourly()
