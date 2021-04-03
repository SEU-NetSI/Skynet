import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
import time
import logging
import pandas as pd
import sys
from utils import log_ranging


if __name__ == '__main__':
    
    uri_id = sys.argv[1]
    log_name = sys.argv[2]
    uri = 'radio://0/' + uri_id + '/2M'

    log_var = {
        'notolsr':'int16_t',
        'recvcountgt':'int16_t',
        'recvcount':'int16_t',
        # 'stateEstimate.z':'float',
    }

    log_ranging(link_uri=uri,log_cfg_name='Packagelost',log_var=log_var,period_in_ms = 100,keep_time_in_s=10)
