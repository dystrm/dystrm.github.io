from test_tweet import post_to_x
from youtube import get_youtube_view_count
from utils import push_to_github
from config import TITLE

import json, os
import subprocess
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../js/data")

PLATFORMS = {
    "melon_top": "멜론 Top 100",
    "melon_hot": "멜론 Hot 100",
    "melon_realtime": "멜론 실시간",
    "genie": "지니",
    "bugs": "벅스",
    "flo": "플로",
    "vibe": "바이브"
}

def load_latest_rank(platform):
    try:
        path = os.path.join(DATA_DIR, f"{platform}.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)["history"]

        now = datetime.now()
        today = now.date()
        today_7 = datetime.combine(today, datetime.min.time()).replace(hour=7)
        yesterday_7 = today_7 - timedelta(days=1)

        if platform == "vibe":
            def find_at(dt):
                return next(
                    (d["rank"] for d in data
                     if datetime.fromisoformat(d["timestamp"]).strftime("%Y-%m-%d %H") == dt.strftime("%Y-%m-%d %H")),
                    None
                )

            if now.hour < 7:
                prev = find_at(yesterday_7)
                return prev, None
            elif now.hour == 7:
                curr = find_at(today_7)
                prev = find_at(yesterday_7)
                return curr, prev
            else:
                curr = find_at(today_7)
                return curr, None

        if len(data) >= 2:
            return data[-1]["rank"], data[-2]["rank"]
        elif len(data) == 1:
            return data[-1]["rank"], None
        else:
            return None, None

    except Exception as e:
        print(f"[ERROR] load_latest_rank({platform}): {e}")
        return None, None


def format_change(curr, prev, platform=None):
    if curr is None:
        return "❌"

    now_hour = datetime.now().hour

    if platform == "melon_top" and now_hour == 1:
        return ""

    if platform == "vibe" and now_hour != 7:
        return "(-)"

    if prev is None:
        return "🆕"

    diff = curr - prev
    if diff == 0:
        return "(-)"
    elif diff > 0:
        return f"(🔻{diff})"
    else:
        return f"(🔺{abs(diff)})"


def build_message():
    now = datetime.now().strftime("%y%m%d %H") + ":00"
    lines = [f"💫 {TITLE} | {now}", ""]

    for key, label in PLATFORMS.items():
        curr, prev = load_latest_rank(key)
        change_str = format_change(curr, prev, key)
        lines.append(f"{label} {curr} {change_str}" if curr else f"{label} ❌")

    hashtags = [
        "#도영 #DOYOUNG"
    ]
    lines.extend(hashtags)

    return "\n".join(lines)


def main():
    tweet = build_message()
    print("[DEBUG] 트윗 내용:", tweet)

    now_hour = datetime.now().hour

    # 02~06시 중단
    if 2 <= now_hour < 7:
        print(f"[X] {now_hour}시: 트윗 전송 시간 아님. 생략.")
        #push_to_github()
        return

    # Playwright 자동 트윗 시간 (22, 23, 00, 01)
    if now_hour in [10, 11, 0, 1]:
        print(f"{now_hour}시: Playwright 트윗 전송 시작")

        # tweet.txt 저장 (내용 전체 유지)
        with open("tweet.txt", "w", encoding="utf-8") as f:
            f.write(tweet)

        result = subprocess.run(
            ["python", "test_tweet.py", "tweet.txt"],
            capture_output=True,
            text=True
        )

        print("[DEBUG] STDOUT:", result.stdout.strip())
        print("[DEBUG] STDERR:", result.stderr.strip())

        push_to_github()
        return

    # 그 외 시간 → API
    try:
        post_to_x(tweet)
    except Exception as e:
        print(f"[X] API 트윗 오류: {e}")

    push_to_github()


if __name__ == "__main__":
    main()
