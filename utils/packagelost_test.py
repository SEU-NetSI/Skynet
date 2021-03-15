# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
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

packgelost_data = [0, 0, 0]


def packagelost_pos_callback(timestamp, data, logconf):
    print(data)
    global packgelost_data
    packgelost_data[0] = data['Packagelost.notolsr']
    packgelost_data[1] = data['Packagelost.recvcountgt']
    packgelost_data[2] = data['Packagelost.recvcount']

    fd.write("notolsr:" + str(packgelost_data[0]))
    fd.write("recvcountgt:" + str(packgelost_data[1]))
    fd.write("recvcount:" + str(packgelost_data[2]))
    fd.write("\r\n")


if __name__ == '__main__':
    uri = 'radio://0/' + sys.argv[1] + '/2M'
    logname = sys.argv[2]

    fd = open("./log/" + logname + ".log", "w+")
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        logconf = LogConfig(name='Stabilizer', period_in_ms=10)
        logconf.add_variable('Packagelost.notolsr', 'int16_t')
        logconf.add_variable('Packagelost.recvcountgt', 'int16_t')
        logconf.add_variable('Packagelost.recvcount', 'int16_t')
        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(packagelost_pos_callback)
        logconf.start()
        # We take off when the commander is created
        with MotionCommander(scf, default_height=0.5) as mc:
            time.sleep(10)
            mc.stop()
            # We land when the MotionCommander goes out of scope
        logconf.stop()
