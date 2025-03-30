import time
import math

import module.thread_main.subject as car
import module.thread_main.information as info

def auto_smoothBrake() :
    info.message = "$$$$ 감속 중"
    while ((math.floor(car.rpm) > math.floor(car.idle_rpm))) :
        car.throttle *= 0.90
        time.sleep(0.01)

    car.message = ""
    car.is_assist_active = False