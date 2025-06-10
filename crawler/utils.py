from datetime import datetime
import subprocess
import json
import os
import re
import requests
from config import TITLE, ARTIST, DISCORD_WEBHOOK_URL, DISCORD_ALERT_ENABLED

# 로그 출력
def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}")

# 크롤링 시각 기록 (공통 Last Update)
def save_last_update():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../js/data"))
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, "last_update.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"last_updated": now}, f, ensure_ascii=False, indent=2)

# 문자열 정규화 (곡명/아티스트 비교용)
def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\s+", "", text)             # 공백 제거
    text = re.sub(r"[()\[\]{}]", "", text)      # 괄호 제거
    text = re.sub(r"[^a-z0-9가-힣/]", "", text)  # 특수문자 제거
    return text

# 순위 데이터 저장
def save_chart(platform, rank):
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../js/data"))
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, f"{platform}.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"title": TITLE, "artist": ARTIST, "history": []}

    now = datetime.now()
    timestamp = now.isoformat()
    this_hour_key = now.replace(minute=0, second=0, microsecond=0).isoformat()

    # 같은 시각 데이터 중복 저장 방지
    for entry in data["history"]:
        entry_hour = entry["timestamp"][:13]
        now_hour = this_hour_key[:13]
        if entry_hour == now_hour:
            return  # 이미 기록됨

    data["history"].append({
        "timestamp": timestamp,
        "rank": rank if rank not in [None, "X"] else None
    })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 디스코드 알림
def send_discord_alert(message):
    if not DISCORD_ALERT_ENABLED:
        return

    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        res.raise_for_status()
        print("📢 디스코드 알림 전송 완료")
    except Exception as e:
        print(f"❌ 디스코드 전송 실패: {e}")

# GitHub 푸시
def push_to_github():
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"[자동업데이트] 차트 데이터 갱신: {now}"

    try:
        # 원격 최신 내용 병합 (자동 merge)
        subprocess.run(["git", "pull", "origin", "main"], check=True)

        # 변경사항 스테이징
        subprocess.run(["git", "add", "."], check=True)

        # 변경 사항 있는지 확인
        result = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if result.returncode == 0:
            print("✅ Git 변경 사항 없음 (스테이징된 변경 없음). 푸시 생략")
            return

        # 커밋 및 푸시
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "push"], check=True)
        print("✅ GitHub 푸시 완료!")

    except subprocess.CalledProcessError as e:
        error_msg = f"GitHub 명령 실패 ❌\n{e}"
        print(f"❌ {error_msg}")
        send_discord_alert(error_msg)

    except Exception as e:
        error_msg = f"GitHub 일반 오류 ❌\n{e}"
        print(f"❌ {error_msg}")
        send_discord_alert(error_msg)

# 단독 테스트용
# if __name__ == "__main__":
#     send_discord_alert("✅ 디스코드 알림 테스트 메시지\n이 메시지가 보이면 연동 정상입니다.")
