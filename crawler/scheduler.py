import schedule
import time
import subprocess
from datetime import datetime
import sys

print(f"⏳ 스케줄러 시작됨")

def job_hourly():
    print("[⏰] 정각+2분: 크롤링 & 트윗")
    subprocess.run(["python", "crawl_hourly.py"])
    subprocess.run(["python", "main_post.py"])

def job_vibe_daily():
    print("[⏰] 07:02 VIBE 포함 전체 크롤링 & 트윗")
    subprocess.run(["python", "crawl_all.py"])
    subprocess.run(["python", "main_post.py"])

def job_test_playwright():
    print("[🧪] 테스트용 Playwright 트윗 실행")
    test_tweet = '💙 테스트 트윗 2025-05-30 12:05\n멜론 Top 100 20위 (🔺3)\n🎬 6,801,210'

    with open("tweet.txt", "w", encoding="utf-8") as f:
        f.write(test_tweet)

    result = subprocess.run(
        ["python", "playwright_tweet.py", "tweet.txt"],
        capture_output=True,
        text=True
    )

    print("[DEBUG] STDOUT:", result.stdout)
    print("[DEBUG] STDERR:", result.stderr)

# 정규 스케줄 설정
for hour in range(24):
    if hour != 7:
        schedule.every().day.at(f"{hour:02d}:11").do(job_hourly)

schedule.every().day.at("07:10").do(job_vibe_daily)

# 루프 실행
while True:
    schedule.run_pending()
    time.sleep(1)
