import cv2
import numpy as np
import math


class MediapipeBody():

    BODY_KEYPOINTS = ["NOSE",
                      "LEFT_EYE_INNER",
                      "LEFT_EYE",
                      "LEFT_EYE_OUTER",
                      "RIGHT_EYE_INNER",
                      "RIGHT_EYE",
                      "RIGHT_EYE_OUTER",
                      "LEFT_EAR",
                      "RIGHT_EAR",
                      "MOUTH_LEFT",
                      "MOUTH_RIGHT",
                      "LEFT_SHOULDER",
                      "RIGHT_SHOULDER",
                      "LEFT_ELBOW",
                      "RIGHT_ELBOW",
                      "LEFT_WRIST",
                      "RIGHT_WRIST",
                      "LEFT_PINKY",
                      "RIGHT_PINKY",
                      "LEFT_INDEX",
                      "RIGHT_INDEX",
                      "LEFT_THUMB",
                      "RIGHT_THUMB",
                      "LEFT_HIP",
                      "RIGHT_HIP",
                      "LEFT_KNEE",
                      "RIGHT_KNEE",
                      "LEFT_ANKLE",
                      "RIGHT_ANKLE",
                      "LEFT_HEEL",
                      "RIGHT_HEEL",
                      "LEFT_FOOT_INDEX",
                      "RIGHT_FOOT_INDEX"]

    BODY_VECTORS = {"SHOULDER_ELBOW_L": ["LEFT_SHOULDER", "LEFT_ELBOW"],
                    "SHOULDER_ELBOW_R": ["RIGHT_SHOULDER", "RIGHT_ELBOW"],
                    "ELBOW_WRIST_L": ["LEFT_ELBOW", "LEFT_WRIST"],
                    "ELBOW_WRIST_R": ["RIGHT_ELBOW", "RIGHT_WRIST"],
                    "HIP_KNEE_L": ["LEFT_HIP", "LEFT_KNEE"],
                    "HIP_KNEE_R": ["RIGHT_HIP", "RIGHT_KNEE"],
                    "KNEE_ANKLE_L": ["LEFT_KNEE", "LEFT_ANKLE"],
                    "KNEE_ANKLE_R": ["RIGHT_KNEE", "RIGHT_ANKLE"],

                    }

    BODY_JOINTS = {"LEFT_ELBOW": ["SHOULDER_ELBOW_L", "ELBOW_WRIST_L"],
                   "LEFT_KNEE": ["HIP_KNEE_L", "KNEE_ANKLE_L"],
                   "RIGHT_KNEE": ["HIP_KNEE_R", "KNEE_ANKLE_R"],
                   "RIGHT_ELBOW": ["SHOULDER_ELBOW_R", "ELBOW_WRIST_R"],
                   }

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        import mediapipe as mp
        self.mp_pose = mp.solutions.pose
        self.skeleton_detection = self.mp_pose.Pose(
            static_image_mode=True, model_complexity=2, enable_segmentation=True, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def getBodyInfo(self, img):
        self.landmarks = self.getBody(img)
        print(self.landmarks)
        self.vectors = self.getBodyVectors()
        self.angles = self.getAnglesFromVectors()

        return self.landmarks, self.vectors, self.angles

    def __points2vector(self, tail, head):
        return (np.array(head) - np.array(tail))

    def __getAngle(self, vector1, vector2):
        inner_product = np.inner(vector1, vector2)
        norm_v1 = np.linalg.norm(vector1)
        norm_v2 = np.linalg.norm(vector2)

        if norm_v1 == 0.0 or norm_v2 == 0.0:
            return np.nan
        cos = inner_product / (norm_v1*norm_v2)
        # result in radians
        rad = np.arccos(np.clip(cos, -1.0, 1.0))
        # covert to degrees
        theta = np.rad2deg(rad)
        return theta

    def getBodyVectors(self):

        self.vectors = {}
        self.vectors_np = {}

        for vector_name, points in self.BODY_VECTORS.items():
            try:
                self.vectors_np[vector_name] = self.__points2vector(
                    tail=self.landmarks[points[0]], head=self.landmarks[points[1]])
                self.vectors[vector_name] = self.vectors_np[vector_name].tolist()
            except:
                self.vectors_np[vector_name] = [0,0,0]

        return self.vectors

    def getAnglesFromVectors(self):
        self.angles = {}
        for vector_name, value in self.BODY_JOINTS.items():
            vector1 = self.vectors_np[value[0]]
            vector2 = self.vectors_np[value[1]]
            self.angles[vector_name] = self.__getAngle(vector1, vector2)

        return self.angles

    def drawLandmarks(self, image_src):
        new_image = image_src.copy()
        self.mp_drawing.draw_landmarks(
            new_image,
            self.body_results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())

        return new_image

    def getBody(self, image_src):
        image_src.flags.writeable = False
        image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB)
        self.body_results = self.skeleton_detection.process(image_src)
        y_resolution, x_resolution, c = image_src.shape
        image_src = cv2.cvtColor(image_src, cv2.COLOR_RGB2BGR)
        # Draw the pose annotation on the image.
        image_src.flags.writeable = True
        pose_values = {}

        for element in self.BODY_KEYPOINTS:
            try:
                value = self.body_results.pose_landmarks.landmark[self.mp_pose.PoseLandmark[element]]
                pose_values[element] = [value.x, value.y, value.z]
            except:
                pass

        return pose_values


"""
# OpenCV code
import cv2
img = cv2.imread('yoga.jpg')
h = MediapipeBody();
landmarks, vectors, angles = h.getBodyInfo(img)

# Display image with drawing hands

cv2.imshow("Result", h.drawLandmarks(img))
cv2.waitKey(0)
"""
