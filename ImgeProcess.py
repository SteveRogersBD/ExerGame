import cv2 as cv
import numpy as np
import mediapipe as mp
import time

class ImageProcess:
    def __init__(self,detect_con=0.5, tracking_con=0.5):
        self.detect_con=detect_con
        self.tracking_con=tracking_con
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.mp_hand = mp.solutions.hands

        #the detectors with attributes
        self.hand_detector=self.mp_hand.Hands(min_detection_confidence=self.detect_con,
                                              min_tracking_confidence=self.tracking_con)


        self.pose_detector = self.mp_pose.Pose(min_detection_confidence=self.detect_con,
                                                  min_tracking_confidence=self.tracking_con)
        self.res_hand=None
        self.res_pose=None
        self.body_positions=[]
        self.hand_positions=[]

    def process_image(self, frame):
        # Convert frame to RGB
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # Process the frame and store results
        self.res_hand = self.hand_detector.process(image)
        self.res_pose = self.pose_detector.process(image)

        height, width, channels = frame.shape
        if self.res_hand.multi_hand_landmarks:
            for lm in self.res_hand.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, lm, self.mp_hand.HAND_CONNECTIONS)
                self.hand_positions = lm.landmark

        if self.res_pose.pose_landmarks:
            self.mp_drawing.draw_landmarks(frame, self.res_pose.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            self.body_positions = self.res_pose.pose_landmarks.landmark

        self.clapped(frame, height, width)
        return frame

    def clapped(self, frame, height, width):
        if len(self.body_positions) > 15:  # Ensure enough landmarks are present
            # Get the landmarks
            x1, y1 = int(self.body_positions[15].x * width), int(self.body_positions[15].y * height)
            x2, y2 = int(self.body_positions[16].x * width), int(self.body_positions[16].y * height)  # Use a different landmark for comparison

            # Calculate the distance
            dist = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            if dist <= 15:
                print("Clapped")


