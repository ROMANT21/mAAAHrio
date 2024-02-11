import threading

import numpy as np

import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles

class Controller:
  def __init__(self):
    self.vid = cv2.VideoCapture(0)
    self.vid.set(3,400)
    self.vid.set(4,400)

    self.frame = None
    self.landmarks = None

    self.thread1 = threading.Thread(target = self.grabFrame)
    self.alive = True

    # Controller controls
    self.jump = False
    self.right = False
    self.left = False

  def destroy(self):
    self.alive = False
    self.vid.release()

  def grabFrame(self):
    while self.alive: 
      
      # Get image
      __, self.frame = self.vid.read()
      time.sleep(1 / 30)
      self.frame = cv2.flip(self.frame, 1)
      self.frame = cv2.line(self.frame, (0, int(self.frame.shape[0] * .70)), (self.frame.shape[1], int(self.frame.shape[0] * .70)), (0, 255, 0), 1) 
      self.frame = cv2.line(self.frame, (0, int(self.frame.shape[0] * 0.30)), (self.frame.shape[1], int(self.frame.shape[0] * 0.30)), (255, 0, 0), 1)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      
      # Label image
      with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
          results = pose.process(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
      mp_drawing.draw_landmarks(
          self.frame,
          results.pose_landmarks,
          mp_pose.POSE_CONNECTIONS,
          landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

      if results.pose_landmarks != None:
          # Is moving
          self.landmarks = results.pose_landmarks
          l_x = self.landmarks.landmark[26].x
          l_y = self.landmarks.landmark[26].y

          r_x = self.landmarks.landmark[25].x
          r_y = self.landmarks.landmark[25].y

          j_r = self.landmarks.landmark[20].y
          j_l = self.landmarks.landmark[21].y

          if r_x > 0.5 and r_y < 0.70:
             self.right = True
          else:
             self.right = False

          if l_x < 0.5 and l_y < 0.70:
             self.left = True
          else:
             self.left = False

          if j_r < 0.3 and j_l < 0.3:
             self.jump = True
          else:
             self.jump = False


          




      cv2.imshow('frame', self.frame)

    print("Threading stopped")

  def startThread(self, gameOver):
    self.thread1.start()

  

if __name__ == "__main__":
  myController = Controller()

  time.sleep(3)
  while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('frame', myController.frame)
    
    print(myController.frame)
  