import time

import module.thread_main.subject as car
import module.thread_main.dataAnalysis as da

message = ""
mutex_message = False

def print_dashboard() :
    global message
    
    while (car.is_drive_active == True) :           
        print("throtle %d %% (prev %d %%)   %d RPM    %s" % (car.throttle, da.prev_throttle, car.rpm, message))
        time.sleep(0.01)