import cv2
import os
import time
import module.thread_main.subject as car

# mutex
mutex_cam = False

# 웹캠 실행
cam = cv2.VideoCapture(0)

# 경로 설정
path_rsrc = "C:/Users/labRat1304/Desktop/incar_definitive/rsrc/cam/"

def cam_cycle() :
    global mutex_cam
    
    # 사진 번호 (1~5를 순환)
    index = 0
    
    while (car.is_drive_active == True) :
        while (mutex_cam == True) :
            time.sleep(0.01)
        mutex_cam = True
        
        ret, frame = cam.read()
        if ret:
            file_path = os.path.join(path_rsrc, f"webcam_screenshot_{index}.jpg")
            cv2.imwrite(file_path, frame)
            #print(f"이미지가 {file_path}에 저장되었습니다.")

            # 다음 파일 번호 (1~5 순환)
            index = (index + 1) % 5

        mutex_cam = False
        time.sleep(0.1)  # 10ms 대기
    

