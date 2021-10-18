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

import logging

import time



import cflib.crtp

from cflib.crazyflie import Crazyflie

from cflib.crazyflie.log import LogConfig

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.positioning.motion_commander import MotionCommander





URI = 'radio://0/100/2M/E7E7E7E7E7'



# DEFAULT_HEIGHT = 1.0



if __name__ == '__main__':

    cflib.crtp.init_drivers(enable_debug_driver=False)



    with SyncCrazyflie(URI) as scf:

        

        # with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:

        cf = scf.cf

        # Set solid color effect

        while(1):

            cf.param.set_value('ring.effect', '7')

            

            time.sleep(2)

            # mc.forward(0.5)



            # Set the RGB values

            cf.param.set_value('ring.solidRed', '100')

            cf.param.set_value('ring.solidGreen', '0')

            cf.param.set_value('ring.solidBlue', '0')

            

            time.sleep(2)

            # mc.turn_left(180)

            

            cf.param.set_value('ring.solidRed', '0')

            cf.param.set_value('ring.solidGreen', '100')

            cf.param.set_value('ring.solidBlue', '0')

            

            time.sleep(2)

            # mc.forward(0.5)



            cf.param.set_value('ring.solidRed', '0')

            cf.param.set_value('ring.solidGreen', '0')

            cf.param.set_value('ring.solidBlue', '100')

        

        time.sleep(1)

