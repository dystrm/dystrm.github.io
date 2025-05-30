from datetime import datetime
from x_poster import post_to_x
from youtube import get_youtube_view_count
from utils import push_to_github
from config import DISCORD_ALERT_ENABLED
from utils import send_discord_alert
from config import TITLE
import json, os
import subprocess

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

        if platform == "vibe":
            today = datetime.now().date().isoformat()
            today_data = [d for d in data if d["timestamp"].startswith(today)]
            if len(today_data) >= 2:
                return today_data[-1]["rank"], today_data[0]["rank"]
            elif len(today_data) == 1:
                return today_data[0]["rank"], today_data[0]["rank"]
            else:
                return None, None

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
    print("[DEBUG] 트윗 내용 (앞부분):", tweet[:50])

    now_hour = datetime.now().hour

    # 테스트 강제 Playwright용: 12시에 강제로 실행
    #FORCE_PLAYWRIGHT = now_hour == 12

    # 새벽 시간대 (2~6시) 자동 생략
    if 2 <= now_hour < 7:
        print(f"[X] {now_hour}시: 트윗 전송 시간 아님. 생략.")
        if DISCORD_ALERT_ENABLED:
            send_discord_alert(
                f"😴 {now_hour}시 차트 트윗은 자동 생략되었습니다.\n(리밋 방지를 위해 새벽 2~6시는 생략됩니다)\n\n📢 트윗 예정 내용:\n{tweet}"
            )
        push_to_github()
        return

    # Playwright로 전송 (0시, 1시, or 테스트 시)
    elif now_hour in [0, 1]:
        print(f"[🌙] {now_hour}시: Playwright로 트윗 전송 시도")
        try:
            # 트윗 텍스트 파일 저장
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
                if DISCORD_ALERT_ENABLED:
                    send_discord_alert(f"[Playwright] {now_hour}시 트윗 전송 완료!\n\n📢 트윗 내용:\n{tweet}")
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

    # API 방식 전송 (07~23시, 12시 제외)
    try:
        post_to_x(tweet)
    except Exception as e:
        print(f"[X] API 트윗 전송 중 오류 발생: {e}")
        if DISCORD_ALERT_ENABLED:
            send_discord_alert(f"❌ API 트윗 전송 실패: {e}\n\n📢 트윗 내용:\n{tweet}")

    push_to_github()

if __name__ == "__main__":
    main()
