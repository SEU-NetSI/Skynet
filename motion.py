import sys
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander


def basic_flying(link_uri, flying_time_in_s=30, flying_height_in_m=0.5):
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(link_uri=link_uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        with MotionCommander(scf, default_height=flying_height_in_m) as mc:
            end_time = time.time() + flying_time_in_s
            while time.time() < end_time:
                continue

            time.sleep(10)
            mc.stop()


if __name__ == '__main__':
    # crazyflie channel
    uri_id = sys.argv[1]

    basic_flying(link_uri='radio://0/' + uri_id + '/2M')
