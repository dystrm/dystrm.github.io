from datetime import datetime
from x_poster import post_to_x
from youtube import get_youtube_view_count
from utils import push_to_github
from config import TITLE
import json
import os

DATA_DIR = "../js/data"

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

        if platform == "vibe":
            today = datetime.now().date().isoformat()
            today_data = [d for d in data if d["timestamp"].startswith(today)]

            if len(today_data) >= 2:
                return today_data[-1]["rank"], today_data[0]["rank"]  # 최신 vs 오늘 아침
            elif len(today_data) == 1:
                rank = today_data[0]["rank"]
                return rank, rank  # 변동 없음
            else:
                return None, None

        # 일반 차트는 마지막 2개 비교
        if len(data) >= 2:
            return data[-1]["rank"], data[-2]["rank"]
        elif len(data) == 1:
            return data[-1]["rank"], None
        else:
            return None, None
    except:
        return None, None


def format_change(curr, prev):
    if curr is None:
        return "❌"
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
    now = datetime.now().strftime("%Y-%m-%d %H:00")
    lines = [f"💙 \"{TITLE}\" {now}"]

    for key, label in PLATFORMS.items():
        curr, prev = load_latest_rank(key)
        if curr is None and prev is None:
            lines.append(f"{label} ❌")
        else:
            change_str = format_change(curr, prev)
            lines.append(f"{label} {curr if curr else '❌'} {change_str}")

    mv_views = get_youtube_view_count()
    lines.append(f"\n🎬 {mv_views:,}")
    return "\n".join(lines)

def main():
    tweet = build_message()
    print("[DEBUG] 트윗 내용:\n", tweet)
    post_to_x(tweet)
    push_to_github()

if __name__ == "__main__":
    main()

