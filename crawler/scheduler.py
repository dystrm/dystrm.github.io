import schedule
import time
import subprocess

def job_hourly():
    print("[⏰] 정각+3분: 크롤링 & 트윗")
    subprocess.run(["python", "crawl_hourly.py"])
    subprocess.run(["python", "main_post.py"])

def job_vibe_daily():
    print("[⏰] 07:03 VIBE 포함 전체 크롤링 & 트윗")
    subprocess.run(["python", "crawl_all.py"])
    subprocess.run(["python", "main_post.py"])

# ✅ 07시는 제외
for hour in range(24):
    if hour != 7:
        schedule.every().day.at(f"{hour:02d}:03").do(job_hourly)

# ✅ 07:03은 VIBE 포함 전용
schedule.every().day.at("07:03").do(job_vibe_daily)

if __name__ == "__main__":
    print("⏳ 스케줄러 시작됨")
    while True:
        schedule.run_pending()
        time.sleep(1)
