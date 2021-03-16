import sys
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.motion_commander import MotionCommander
import pandas as pd


def log_flying(link_uri, log_cfg_name='Packagelost', log_var={}, log_save_path="./default.csv", period_in_ms=100,
                keep_time_in_s=20):
    cflib.crtp.init_drivers(enable_debug_driver=False)
    log_data = pd.DataFrame(columns=log_var.keys())

    with SyncCrazyflie(link_uri=link_uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        log_cfg = LogConfig(name=log_cfg_name, period_in_ms=period_in_ms)
        for log_var_name, log_var_type in log_var.items():
            log_cfg.add_variable(log_cfg.name + '.' + log_var_name, log_var_type)

        with MotionCommander(scf, default_height=0.5) as mc:
            with SyncLogger(scf, log_cfg) as logger:
                end_time = time.time() + keep_time_in_s
                while time.time() < end_time:
                    continue
                for i in range(logger._queue.qsize()):
                    log_entry = logger.next()
                    timestamp = log_entry[0]
                    data = log_entry[1]
                    logconf_name = log_entry[2]

                    temp = {}
                    temp['timestamp'] = timestamp
                    for log_var_name, log_var_type in log_var.items():
                        temp[log_var_name] = data[log_cfg.name + '.' + log_var_name]

                    log_data = log_data.append(temp, ignore_index=True)
                    print(temp)

                    log_data.to_csv(log_save_path, index=False)
            
            time.sleep(10)
            mc.stop()


if __name__ == '__main__':

    uri_id = sys.argv[1]
    csv_name = sys.argv[2]
    uri = 'radio://0/' + uri_id + '/2M'
    csv_path = "./csv/" + csv_name + ".csv"

    log_var = {
        'notolsr':'int16_t',
        'recvcountgt':'int16_t',
        'recvcount':'int16_t'
    }

    log_flying(link_uri=uri,log_var=log_var,log_save_path=csv_path)