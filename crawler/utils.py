import datetime
import subprocess
import json
import os
import requests
from config import TITLE, ARTIST
from config import DISCORD_WEBHOOK_URL

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def save_chart(platform, rank):
    data_dir = "../js/data"
    os.makedirs(data_dir, exist_ok=True)
    filename = f"{platform}.json"
    path = os.path.join(data_dir, filename)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"title": TITLE, "artist": ARTIST, "history": []}

    now = datetime.datetime.now()
    timestamp = now.isoformat()
    this_hour_key = now.replace(minute=0, second=0, microsecond=0).isoformat()

    # ✅ 중복 여부 확인 (같은 시각 데이터가 이미 있을 경우)
    for entry in data["history"]:
        entry_hour = entry["timestamp"][:13]  # "YYYY-MM-DDTHH"
        now_hour = this_hour_key[:13]
        if entry_hour == now_hour:
            return  # 이미 해당 시각에 기록됨

    data["history"].append({
        "timestamp": timestamp,
        "rank": rank if rank not in [None, "X"] else None
    })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

        

def send_discord_alert(message):
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🚨 {message}"})
        res.raise_for_status()
        print("📢 디스코드 알림 전송 완료")
    except Exception as e:
        print(f"❌ 디스코드 전송 실패: {e}")


def push_to_github():
    # 루트 디렉토리 이동
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"[자동업데이트] 차트 데이터 갱신: {now}"

    try:
        # add 실행
        subprocess.run(["git", "add", "."], check=True)

        # 변경사항 확인 (스테이징된 것 기준)
        result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if result.returncode == 0:
            print("✅ Git 변경 사항 없음 (스테이징된 변경 없음). 푸시 생략")
            return

        # 커밋 및 푸시
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "push"], check=True)
        print("✅ GitHub 푸시 완료!")
        send_discord_alert("✅ GitHub 푸시 완료!")

    except subprocess.CalledProcessError as e:
        error_msg = f"GitHub 푸시 실패 ❌\n{e}"
        print(f"❌ {error_msg}")
        send_discord_alert(error_msg)

    except Exception as e:
        error_msg = f"GitHub 일반 오류 ❌\n{e}"
        print(f"❌ {error_msg}")
        send_discord_alert(error_msg)

if __name__ == "__main__":
    send_discord_alert("✅ 디스코드 알림 테스트 메시지\n이 메시지가 보이면 연동 정상 확인.")