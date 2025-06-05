from x_poster import post_to_x
from youtube import get_youtube_view_count
from utils import push_to_github
from config import DISCORD_ALERT_ENABLED
from utils import send_discord_alert
from config import TITLE
import json, os
import subprocess
from datetime import datetime, timedelta

# 절대경로 설정
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
    if prev is None:
        return "🆕"
    if platform == "vibe" and datetime.now().hour != 7:
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
    lines = [f"💙 \"{TITLE}\" {now}", ""]

    for key, label in PLATFORMS.items():
        curr, prev = load_latest_rank(key)
        if curr is None:
            lines.append(f"{label} ❌")
        else:
            change_str = format_change(curr, prev, key)
            lines.append(f"{label} {curr} {change_str}")

    mv_views = get_youtube_view_count()
    lines.append(f"\n🎬 {mv_views:,}")
    return "\n".join(lines)

def main():
    tweet = build_message()
    print("[DEBUG] 트윗 내용 (앞부분):", tweet)

    now_hour = datetime.now().hour

    if 2 <= now_hour < 7:
        print(f"[X] {now_hour}시: 트윗 전송 시간 아님. 생략.")
        if DISCORD_ALERT_ENABLED:
            send_discord_alert(
                f"😴 {now_hour}시 차트 생략, 트윗 전송 시간 07~01시"
            )
        push_to_github()
        return

    elif now_hour in [0, 1]:
        print(f"[🌙] {now_hour}시: Playwright로 트윗 전송 시도")
        try:
            with open("tweet.txt", "w", encoding="utf-8") as f:
                f.write(tweet)

            result = subprocess.run(
                ["python", "playwright_tweet.py", "tweet.txt"],
                capture_output=True,
                text=True
            )

            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            print("[DEBUG] STDOUT:", stdout)
            print("[DEBUG] STDERR:", stderr)

            if "트윗 전송 성공" in stdout:
                print("[Playwright] 트윗 전송 성공 로그 감지")
                #if DISCORD_ALERT_ENABLED:
                    #send_discord_alert(f"[Playwright] {now_hour}시 트윗 전송 완료!\n\n📢 트윗 내용:\n{tweet}")
            else:
                print("[X] Playwright 트윗 실패 로그 감지")
                if DISCORD_ALERT_ENABLED:
                    send_discord_alert(f"[Playwright] 트윗 실패 로그 감지\n\n📢 트윗 내용:\n{tweet}\n\n📄 로그:\n{stdout or stderr}")

        except Exception as e:
            print(f"[X] Playwright 트윗 예외 발생: {e}")
            if DISCORD_ALERT_ENABLED:
                send_discord_alert(f"[Playwright] 트윗 예외 발생: {e}\n\n📢 트윗 내용:\n{tweet}")

        push_to_github()
        return

    try:
        post_to_x(tweet)
    except Exception as e:
        print(f"[X] API 트윗 전송 중 오류 발생: {e}")
        if DISCORD_ALERT_ENABLED:
            send_discord_alert(f"❌ API 트윗 전송 실패: {e}\n\n📢 트윗 내용:\n{tweet}")

    push_to_github()

if __name__ == "__main__":
    main()
