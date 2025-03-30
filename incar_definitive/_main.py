import threading as th
import time

# Simulation Thread
import module.thread_main.subject as car
import module.thread_main.camera as cam

# Object Threadsf
import module.thread_main.information as info
import module.thread_main.ctrl_user as user
import module.thread_main.dataAnalysis as da
    
listThread = []
listThread.append(th.Thread(target=car.engine))
listThread.append(th.Thread(target=cam.cam_cycle))

listThread.append(th.Thread(target=info.print_dashboard))
listThread.append(th.Thread(target=user.ctrl_user))
listThread.append(th.Thread(target=da.analysis))

for thread in listThread :
    thread.start()

time.sleep(60)