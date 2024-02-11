import math
import numpy as np

import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles

vid = cv2.VideoCapture(0)
vid.set(3,200)
vid.set(4,200)

while(True):
    #inside infinity loop
    ret, frame = vid.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    if results.pose_landmarks != None:
        print(results.pose_landmarks.landmark[25])
    cv2.imshow('frame', frame)


vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

