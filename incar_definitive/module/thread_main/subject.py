import time

# Flags
is_drive_active = True
is_assist_active = False

# Engine param
idle_rpm = 800.0
max_rpm = 7000.0
response_rate = 0.1

# Drive status
throttle = 40
rpm = idle_rpm

def engine() :
    global is_drive_active
    global throttle
    global rpm
    global idle_rpm
    global max_rpm
    global response_rate
    
    while (is_drive_active == True) :
        target_rpm = idle_rpm + (max_rpm - idle_rpm) * (throttle / 100)
        rpm += (target_rpm - rpm) * response_rate        
        time.sleep(0.01)
    
    return