import time
import threading as th

import module.thread_main.subject as car
import module.thread_main.information as info

import module.model_emotion as emot
import module.ctrl_assist as assist

# Time Factor
dur_emotRecog = 2

# Monitored Values
prev_throttle = 0.0

# Flags
is_suddenAcceleration = False

# IMG DATA
is_fromCam = False
name_staticImg = "panic.png"

def _detect_driver_panic() :
    path_rsrc = "C:/Users/labRat1304/Desktop/incar_definitive/rsrc/"
        
    if (is_fromCam == True) :
        for i in range(0, 5) :
            path_cam_i = path_rsrc + f"cam/webcam_screenshot_{i}.jpg"  # f-string 사용
            emote = emot.get_emotion(path_cam_i, path_rsrc + "mymodel.weights.h5")
            if emote == True :
                break
    else :
        emote = emot.get_emotion(path_rsrc + name_staticImg, path_rsrc + "mymodel.weights.h5")

    if (emote == True) :
        emot.message = "! 급가속 ! 급발진"        
        car.is_assist_active = True
            
        subThread = th.Thread(target=assist.auto_smoothBrake)
        subThread.start()
    
def record_prev_throttle() :
    global prev_throttle    
    prev_throttle = car.throttle
    time.sleep(0.01)

def detect_suddenAcceleration() :
    global is_suddenAcceleration
    
    if car.throttle - prev_throttle > 50 and car.rpm > 2500:
        info.message = "! 급가속"
        is_suddenAcceleration = True
        
        subThread = th.Thread(target=_detect_driver_panic)
        subThread.start()
        subThread.join()
    else :
        info.message = ""
        is_suddenAcceleration = False

def analysis() :    
    while (car.is_drive_active == True) :
        record_prev_throttle()
        detect_suddenAcceleration()