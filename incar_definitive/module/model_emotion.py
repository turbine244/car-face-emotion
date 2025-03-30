import os
import tensorflow as tf
import numpy as np
import time


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization

import module.thread_main.camera as cam

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # 경고 및 정보 메시지 숨기기

num_classes = 7
num_detectors = 32
width, height = 48, 48

network = Sequential()

network.add(Conv2D(filters=num_detectors, kernel_size=3, activation='relu', padding='same', input_shape=(width, height, 3)))
network.add(BatchNormalization())
network.add(Conv2D(filters=num_detectors, kernel_size=3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2, 2)))
network.add(Dropout(0.2))

network.add(Conv2D(2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2, 2)))
network.add(Dropout(0.2))

network.add(Conv2D(2*2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(2*2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2, 2)))
network.add(Dropout(0.2))

network.add(Conv2D(2*2*2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(Conv2D(2*2*2*num_detectors, 3, activation='relu', padding='same'))
network.add(BatchNormalization())
network.add(MaxPooling2D(pool_size=(2, 2)))
network.add(Dropout(0.2))

network.add(Flatten())

network.add(Dense(2*2*num_detectors, activation='relu'))
network.add(BatchNormalization())
network.add(Dropout(0.2))

network.add(Dense(2*num_detectors, activation='relu'))
network.add(BatchNormalization())
network.add(Dropout(0.2))

network.add(Dense(num_classes, activation='softmax'))

network.compile(optimizer='Adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

import cv2
import dlib

def get_emotion(img_path, weight_path):
    if cam.mutex_cam == True :
        time.sleep(0.01)
    cam.mutex_cam = True
    
    image = cv2.imread(os.path.abspath(img_path))
    # 가중치만 불러오기
    network.load_weights(os.path.abspath(weight_path))

    #print("dlib version:", dlib.__version__)
    #print("CUDA available?", dlib.DLIB_USE_CUDA)


# Force DLIB to use CPU by setting the environment variable
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Disable CUDA usage within dlib
    dlib.DLIB_USE_CUDA = False

# Load the face detector model, wrap in a try-except block
    try:
        face_detector = dlib.get_frontal_face_detector()
    except RuntimeError as e:
        if "CUDA" in str(e):
            print("Error: Dlib is trying to use CUDA despite being disabled. Check Dlib installation and CUDA settings.")
        # Further debugging or fallback mechanisms can be added here
        else:
            raise e  # Re-raise the exception if it's not CUDA-related


# 얼굴 탐지 실행 (이미지 처리)
    face_detection = face_detector(image, 1)

    if (len(face_detection) == 0) :
        print ("no face detected")
        return False

# 탐지된 얼굴 출력
    #print(f"Number of faces detected: {len(face_detection)}")
    for face in face_detection:
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    left, top, right, bottom = face_detection[0].left(), face_detection[0].top(), face_detection[0].right(), face_detection[0].bottom()

    roi = image[top:bottom, left:right]


    roi.shape

# Resize image
    roi = cv2.resize(roi, (48, 48))

    roi.shape

# Normalize
    roi = roi / 255

    roi = np.expand_dims(roi, axis=0)
    roi.shape

    pred_probability = network.predict(roi, verbose=0)
    emote = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    
    for face in  pred_probability :
        pred = np.argmax(face)
        
        print()
        
        i = 0
        for pr in face :
            print("%s : %f%%" % (emote[i], pr))
            i += 1
        
        print("\n! RESULT : %s (%f%%)\n" % (emote[pred], pred_probability[0][pred]))
        
        if pred == 2 or pred == 6 :
            cam.mutex_cam = False
            return True
    
    cam.mutex_cam = False
    return False