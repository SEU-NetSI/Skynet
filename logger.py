import sys
import time

import cflib.crtp
import pandas as pd
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.motion_commander import MotionCommander


def log_flying(link_uri, log_group_name, log_field_dict=None, log_save_path="./default.csv",
               period_in_ms=100, flying_time_in_s=30, flying_height_in_m=0.5):
    if log_field_dict is None:
        log_field_dict = {}

    cflib.crtp.init_drivers(enable_debug_driver=False)
    log_data = pd.DataFrame(columns=log_field_dict.keys())

    with SyncCrazyflie(link_uri=link_uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        # config the log
        log_cfg = LogConfig(name=log_group_name, period_in_ms=period_in_ms)
        for log_var_name, log_var_type in log_field_dict.items():
            log_cfg.add_variable(log_cfg.name + '.' + log_var_name, log_var_type)

        with MotionCommander(scf, default_height=flying_height_in_m) as mc:
            with SyncLogger(scf, log_cfg) as logger:
                # add a delay for stable logging
                end_time = time.time() + flying_time_in_s
                while time.time() < end_time:
                    continue

                # read log
                for i in range(logger._queue.qsize()):
                    log_entry = logger.next()
                    timestamp = log_entry[0]
                    data = log_entry[1]

                    temp = {'timestamp': timestamp}
                    for log_var_name, log_var_type in log_field_dict.items():
                        temp[log_var_name] = data[log_cfg.name + '.' + log_var_name]

                    log_data = log_data.append(temp, ignore_index=True)
                log_data.to_csv(log_save_path, index=False)
            
            time.sleep(10)
            mc.stop()


def log_static(link_uri, log_group_name, log_field_dict=None, log_save_path="./default.csv",
               period_in_ms=100, testing_time_in_s=30):
    if log_field_dict is None:
        log_field_dict = {}

    cflib.crtp.init_drivers(enable_debug_driver=False)
    log_data = pd.DataFrame(columns=log_field_dict.keys())

    with SyncCrazyflie(link_uri=link_uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        # config the log
        log_cfg = LogConfig(name=log_group_name, period_in_ms=period_in_ms)
        for log_var_name, log_var_type in log_field_dict.items():
            log_cfg.add_variable(log_cfg.name + '.' + log_var_name, log_var_type)

        with SyncLogger(scf, log_cfg) as logger:
            # add a delay for stable logging
            end_time = time.time() + testing_time_in_s
            while time.time() < end_time:
                continue

            # read log
            for i in range(logger._queue.qsize()):
                log_entry = logger.next()
                timestamp = log_entry[0]
                data = log_entry[1]

                temp = {'timestamp': timestamp}
                for log_var_name, log_var_type in log_field_dict.items():
                    temp[log_var_name] = data[log_cfg.name + '.' + log_var_name]

                log_data = log_data.append(temp, ignore_index=True)
            log_data.to_csv(log_save_path, index=False)

        time.sleep(10)


if __name__ == '__main__':
    # crazyflie channel
    uri_id = sys.argv[1]
    # log file name / experiment name
    experiment_name = sys.argv[2]

    # log config
    log_group_name = 'ReceiveRate'
    log_field_dict = {
        'receiveRate': 'float'
    }

    log_static(link_uri='radio://0/' + uri_id + '/2M',
               log_group_name=log_group_name,
               log_field_dict=log_field_dict,
               log_save_path="./csv/" + experiment_name + ".csv")
