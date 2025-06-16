from melon import melon
from genie import get_genie_top200
from bugs import get_bugs_top100
#from flo import get_flo_top100
from flo_mac import get_flo_top100
from vibe import get_vibe_top100
from melon_realtime import melon as melon_realtime
from melon_award import melon_award
from utils import send_discord_alert, save_last_update, pull_from_github, push_to_github

def safe_run(name, func):
    try:
        func()
    except Exception as e:
        print(f"❌ {name} 크롤링 실패: {e}")
        send_discord_alert(f"❌ {name} 크롤링 실패")

def run_all():
    safe_run("멜론 Top", lambda: melon("melon_top"))
    safe_run("멜론 Hot", lambda: melon("melon_hot"))
    safe_run("멜론 실시간", melon_realtime)
    safe_run("지니", get_genie_top200)
    safe_run("벅스", get_bugs_top100)
    safe_run("플로", get_flo_top100)
    safe_run("바이브", get_vibe_top100)
    safe_run("멜론 어워드", melon_award)
    save_last_update()

if __name__ == "__main__":
    pull_from_github()
    run_all()
    push_to_github()
