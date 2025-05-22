from melon import melon
from genie import get_genie_top200
from bugs import get_bugs_top100
from flo import get_flo_top100
from melon_realtime import melon as melon_realtime
from melon_award import melon_award

def run_hourly():
    melon("melon_top")
    melon("melon_hot")
    melon_realtime()
    get_genie_top200()
    get_bugs_top100()
    get_flo_top100()
    melon_award()

if __name__ == "__main__":
    run_hourly()
