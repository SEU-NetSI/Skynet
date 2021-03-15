"""
This script shows the basic use of the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. This script requires some kind of location system, it has been
tested with (and designed for) the flow deck.

The MotionCommander uses velocity setpoints.

Change the URI variable to your Crazyflie configuration.
"""
import logging
import sys
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig

URI = 'radio://0/29/2M'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

packgelost_data = [0, 0, 0, 0, 0]


def packagelost_pos_callback(timestamp, data, logconf):
    print(data)
    global packgelost_data
    packgelost_data[0] = data['Packagelost.notolsr']
    packgelost_data[1] = data['Packagelost.recvcountgt']
    packgelost_data[2] = data['Packagelost.recvcount']
    packgelost_data[3] = data['stateEstimate.z']
    packgelost_data[4] = time.time() - start_time

    fd.write("fly_time:" + str(packgelost_data[4]) + ",")
    fd.write("notolsr:" + str(packgelost_data[0]) + ",")
    fd.write("recvcountgt:" + str(packgelost_data[1]) + ",")
    fd.write("recvcount:" + str(packgelost_data[2]) + ",")
    fd.write("z:" + str(packgelost_data[3]))
    fd.write("\r\n")


if __name__ == '__main__':
    uri_id = sys.argv[1]
    log_name = sys.argv[2]
    uri = 'radio://0/' + uri_id + '/2M'
    log_path = "./log/" + log_name + ".log"
    fd = open(log_path, "w+")

    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        logconf = LogConfig(name='Stabilizer', period_in_ms=25)
        logconf.add_variable('Packagelost.notolsr', 'int16_t')
        logconf.add_variable('Packagelost.recvcountgt', 'int16_t')
        logconf.add_variable('Packagelost.recvcount', 'int16_t')
        logconf.add_variable('stateEstimate.z','float')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(packagelost_pos_callback)
        logconf.start()

        start_time = time.time()
        # We take off when the commander is created
        with MotionCommander(scf, default_height=0.5) as mc:
            time.sleep(20)
            mc.stop()

        # Land when the MotionCommander goes out of scope
        logconf.stop()
