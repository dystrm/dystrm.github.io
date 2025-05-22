import datetime
import subprocess
import json
import os
from config import TITLE, ARTIST

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def save_chart(platform, rank):
    DATA_DIR = "../js/data"
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


def push_to_github():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"[자동업데이트] 차트 데이터 갱신: {now}"

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ GitHub 푸시 완료!")
    except Exception as e:
        print(f"❌ GitHub 푸시 실패: {e}")