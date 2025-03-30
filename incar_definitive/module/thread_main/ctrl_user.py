import time
import keyboard

import module.thread_main.subject as car

def user_throttle() :
    if (keyboard.is_pressed("a")) :
        car.throttle -= 60
            
    if (keyboard.is_pressed("s")) :
        car.throttle -= 1
            
    if (keyboard.is_pressed("d")) :
        car.throttle += 1
            
    if (keyboard.is_pressed("f")) :
        car.throttle += 60            
        
    if (car.throttle < 0) :
            car.throttle = 0
    if (car.throttle > 100) :
        car.throttle = 100

def ctrl_user() :
    while(car.is_drive_active == True) :
        if (car.is_assist_active == False) :
            user_throttle()
            
        time.sleep(0.01)