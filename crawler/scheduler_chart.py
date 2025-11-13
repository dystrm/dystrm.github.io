import schedule
import time
import subprocess
from datetime import datetime
import sys

print("⏳ 크롤링 전용 스케줄러 실행")

# 매시간(정각+10분): 멜론, 지니, 멜론 실시간 등
def job_hourly_crawl():
    print("[⏰] 정각+10분: 시간별 크롤링 실행")
    subprocess.run(["python", "crawl_hourly.py"])
    subprocess.run(["python", "test.py"])

# 매일 07:10: VIBE 포함 전체 크롤링
def job_daily_vibe_crawl():
    print("[⏰] 07:10: VIBE 포함 전체 크롤링 실행")
    subprocess.run(["python", "crawl_all.py"])
    subprocess.run(["python", "test.py"])

# 스케줄 등록
for hour in range(24):
    # 2~6시는 제외 + 07시는 VIBE 전용
    if hour in [2, 3, 4, 5, 6]:
        continue
    if hour == 7:
        continue

    schedule.every().day.at(f"{hour:02d}:10").do(job_hourly_crawl)

# 07:10은 daily vibe
schedule.every().day.at("07:10").do(job_daily_vibe_crawl)

# 루프
while True:
    schedule.run_pending()
    time.sleep(1)
