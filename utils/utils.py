import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
import time
import logging
import pandas as pd

logging.basicConfig(level=logging.ERROR)


def log_ranging(link_uri, log_cfg_name='TSranging', log_var={}, log_save_path="./default.csv", period_in_ms=100,
                keep_time_in_s=5):
    cflib.crtp.init_drivers(enable_debug_driver=False)
    log_data = pd.DataFrame(columns=log_var.keys())

    with SyncCrazyflie(link_uri=link_uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        log_cfg = LogConfig(name=log_cfg_name, period_in_ms=period_in_ms)
        for log_var_name, log_var_type in log_var.items():
            log_cfg.add_variable(log_cfg.name + '.' + log_var_name, log_var_type)

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


def async_log_cb(timestamp, data, logconf):
    print('timestamp:{0}, total_send:{1}, total_receive:{2}, total_compute:{3}'.format(
        timestamp, data['TSranging.total_send'], data['TSranging.total_receive'], data['TSranging.total_compute']))


def async_log_ranging(link_uri, log_cfg_name='TSranging', log_var={}, log_save_path="./default.csv", period_in_ms=100,
                      keep_time_in_s=5):
    cflib.crtp.init_drivers()
    log_data = pd.DataFrame(columns=log_var.keys())

    with SyncCrazyflie(link_uri=link_uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        log_cfg = LogConfig(name=log_cfg_name, period_in_ms=period_in_ms)
        scf.cf.log.add_config(log_cfg)
        for log_var_name, log_var_type in log_var.items():
            log_cfg.add_variable(log_cfg.name + '.' + log_var_name, log_var_type)
        log_cfg.data_received_cb.add_callback(async_log_cb)

        log_cfg.start()
        time.sleep(keep_time_in_s)
        # end_time = time.time() + keep_time_in_s
        # if time.time() > end_time:
        #     log_cfg.stop()