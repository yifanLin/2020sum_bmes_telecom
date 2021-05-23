import sys
import pickle
import cv2
import mediapipe as mp
import pandas as pd
import time
import numpy as np
from socket import *

# Acquire IP for this device, only in use if one wishes to test local transfer
# IP = gethostbyname(gethostname())

# TODO: use your own publicly accessed IP for variable IP
YIFAN_IP = "192.168.1.82"
Yifan_P_IP = "99.76.229.200"
IP = "75.80.53.21"

port = 5075  # If port already in use, try changing it
s1 = socket(AF_INET, SOCK_STREAM)
s1.connect((YIFAN_IP, port))

initial = time.time()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
data = pd.DataFrame()

# For webcam input:
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        # Send data only if one hand is detected
        if len(results.multi_hand_landmarks) == 1:
            hand_landmarks = results.multi_hand_landmarks[0]
            wrist = (hand_landmarks.landmark)[0]
            thumbtip = (hand_landmarks.landmark)[4]
            middletip = (hand_landmarks.landmark)[12]

            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            keypoint_w = tuple({
                wrist.x,
                wrist.y,
                wrist.z,
            })

            keypoint_t = tuple({
                thumbtip.x,
                thumbtip.y,
                thumbtip.z,
            })

            keypoint_m = tuple({
                middletip.x,
                middletip.y,
                middletip.z,
            })

            dict = {"w": keypoint_w, "t": keypoint_t, "m": keypoint_m, "time": time.time() - initial}
            data = data.append(dict, ignore_index=True)

            msg = pickle.dumps(dict)
            s1.sendall(msg)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
hands.close()
cap.release()