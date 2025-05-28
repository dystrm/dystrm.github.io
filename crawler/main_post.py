from datetime import datetime
from x_poster import post_to_x
from youtube import get_youtube_view_count
from utils import push_to_github
from config import DISCORD_ALERT_ENABLED
from utils import send_discord_alert
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
                return today_data[-1]["rank"], today_data[0]["rank"]
            elif len(today_data) == 1:
                rank = today_data[0]["rank"]
                return rank, rank
            else:
                return None, None

        if len(data) >= 2:
            return data[-1]["rank"], data[-2]["rank"]
        elif len(data) == 1:
            return data[-1]["rank"], None
        else:
            return None, None
    except:
        return None, None

def format_change(curr, prev, platform=None):
    if curr is None:
        return "❌"
    if prev is None:
        return "🆕"

    # ✅ VIBE는 07시에만 증감 표시, 나머지 시간엔 (-)
    if platform == "vibe":
        if datetime.now().hour != 7:
            return "(-)"

    diff = curr - prev
    if diff == 0:
        return "(-)"
    elif diff > 0:
        return f"(🔻{diff})"
    else:
        return f"(🔺{abs(diff)})"

def build_message():
    now = datetime.now().strftime("%Y-%m-%d %H시 차트")
    lines = [f"💙 \"{TITLE}\" {now}",""]

    for key, label in PLATFORMS.items():
        curr, prev = load_latest_rank(key)
        if curr is None and prev is None:
            lines.append(f"{label} ❌")
        else:
            change_str = format_change(curr, prev, key)
            lines.append(f"{label} {curr if curr else '❌'} {change_str}")

    mv_views = get_youtube_view_count()
    lines.append(f"\n🎬 {mv_views:,}")
    return "\n".join(lines)

def main():
    tweet = build_message()
    print("[DEBUG] 트윗 내용:\n", tweet)

    now_hour = datetime.now().hour
    if 2 <= now_hour < 7:
        print(f"[X] {now_hour}시: 트윗 전송 시간 아님. 트윗 생략.")

        # ✅ 디스코드 알림도 보냄
        if DISCORD_ALERT_ENABLED:
            send_discord_alert(
                f"😴 {now_hour}시 차트 트윗은 자동 생략되었습니다.\n(리밋 방지를 위해 새벽 2~6시에는 트윗이 올라가지 않아요)\n\n📢 트윗 예정 내용:\n{tweet}"
            )
    else:
        try:
            post_to_x(tweet)
        except Exception as e:
            print(f"[X] 트윗 전송 중 오류 발생: {e}")
            if DISCORD_ALERT_ENABLED:
                send_discord_alert(f"❌ 트윗 전송 중 예외 발생: {e}\n\n📢 트윗 내용:\n{tweet}")

    push_to_github()

if __name__ == "__main__":
    main()
