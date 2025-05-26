from vibe import get_vibe_top100
#from utils import send_discord_alert

try:
    get_vibe_top100()
    print("✅ VIBE 단독 크롤링 완료")
    #send_discord_alert("✅ VIBE 단독 크롤링 테스트 완료!")
except Exception as e:
    print(f"❌ VIBE 크롤링 실패: {e}")
    #send_discord_alert(f"❌ VIBE 크롤링 실패 ❌\n{e}")
