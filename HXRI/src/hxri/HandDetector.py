from turtle import left
import cv2
import numpy as np
import mediapipe as mp


class MediapipeHand():

    landmark_line_ids = [ 
            (0, 1), (1, 5), (5, 9), (9, 13), (13, 17), (17, 0),  
            (1, 2), (2, 3), (3, 4),        
            (5, 6), (6, 7), (7, 8),        
            (9, 10), (10, 11), (11, 12),   
            (13, 14), (14, 15), (15, 16),  
            (17, 18), (18, 19), (19, 20),   
        ]
    
    HAND_KEYPOINTS = ["WRIST",
          "THUMB_CMC",
          "THUMB_MCP" ,
          "THUMB_IP",
          "THUMB_TIP",
          "INDEX_FINGER_MCP",
          "INDEX_FINGER_PIP",
          "INDEX_FINGER_DIP",
          "INDEX_FINGER_TIP",
          "MIDDLE_FINGER_MCP",
          "MIDDLE_FINGER_PIP",
          "MIDDLE_FINGER_DIP",
          "MIDDLE_FINGER_TIP",
          "RING_FINGER_MCP",
          "RING_FINGER_PIP",
          "RING_FINGER_DIP",
          "RING_FINGER_TIP",
          "PINKY_MCP",
          "PINKY_PIP",
          "PINKY_DIP",
          "PINKY_TIP"]
    
    
    dict_points = {"WRIST":{},"THUMB_CMC":{},"THUMB_MCP":{},
          "THUMB_IP":{},"THUMB_TIP":{},
          "INDEX_FINGER_MCP":{},"INDEX_FINGER_PIP":{},
          "INDEX_FINGER_DIP":{},"INDEX_FINGER_TIP":{},
          "MIDDLE_FINGER_MCP":{},"MIDDLE_FINGER_PIP":{},
          "MIDDLE_FINGER_DIP":{},"MIDDLE_FINGER_TIP":{},
          "RING_FINGER_MCP":{},"RING_FINGER_PIP":{},
          "RING_FINGER_DIP":{},"RING_FINGER_TIP":{},
          "PINKY_MCP":{},"PINKY_PIP":{},
          "PINKY_DIP":{},"PINKY_TIP":{}}


    HAND_VECTORS = {"TWC":["WRIST", "THUMB_CMC"],
                "TCM":["THUMB_CMC", "THUMB_MCP"],
                "TMI":["THUMB_MCP", "THUMB_IP"],
                "TIT":["THUMB_IP", "THUMB_TIP"],
                "IWM":["WRIST", "INDEX_FINGER_MCP"],
                "IMP":["INDEX_FINGER_MCP", "INDEX_FINGER_PIP"],
                "IPD":["INDEX_FINGER_PIP", "INDEX_FINGER_DIP"],
                "IDT":["INDEX_FINGER_DIP", "INDEX_FINGER_TIP"],
                "MWM":["WRIST", "MIDDLE_FINGER_MCP"],
                "MMP":["MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"],
                "MPD":["MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"],
                "MDT":["MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP"],
                "RWM":["WRIST", "RING_FINGER_MCP"],
                "RMP":["RING_FINGER_MCP", "RING_FINGER_PIP"],
                "RPD":["RING_FINGER_PIP", "RING_FINGER_DIP"],
                "RDT":["RING_FINGER_DIP", "RING_FINGER_TIP"],
                "PWM":["WRIST", "PINKY_MCP"],
                "PMP":["PINKY_MCP", "PINKY_PIP"],
                "PPD":["PINKY_PIP", "PINKY_DIP"],
                "PDT":["PINKY_DIP", "PINKY_TIP"]
        }

    HAND_JOINTS = {"WRIST_THUMB_INDEX":["TWC","IWM"],
                "WRIST_INDEX":["IWM","IMP"],
                "INDEX_1":["IMP","IPD"],
                "INDEX_2":["IPD","IDT"],
                "WRIST_MIDDLE":["MWM","MMP"],
                "MIDDLE_1":["MMP","MPD"],
                "MIDDLE_2":["MPD","MDT"]
        }

    #dict_joints = {"WRIST_THUMB_INDEX":{},
    #            "WRIST_THUMB":{},
    #            "THUMB_1":{},
    #            "THUMB_2":{},
    #            "WRIST_INDEX":{},
    #            "INDEX_1":{},
    #            "INDEX_2":{},
    #            "INDEX_MIDDLE":{},
    #            "WRIST_MIDDLE":{},
    #            "MIDDLE_1":{},
    #            "MIDDLE_2":{}
    #    }

    def __init__(self):
        self.mp_hands = mp.solutions.hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2)


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

    def getLandmarks(self,img):

        """ Get landmarks from hands 
        
        Parameters
        ----------

        img : cv2 image 
            OpenCV image

        Returns
        ----------

        left : dict
            Left hand data
        right : dict
            Right hand data
        """

        # Convert the BGR image to RGB before processing.
        self.results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        img_h, img_w, _ = img.shape 

        self.left = {"position": self.dict_points.copy(), "score":0}
        self.right = {"position": self.dict_points.copy(), "score":0} 
        image_points = None

        if self.results.multi_hand_landmarks:
            image_points = self.results.multi_hand_landmarks
            for h_id, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
                for c_id, hand_class in enumerate(self.results.multi_handedness[h_id].classification):
                    label = hand_class.label
                    if label == "Right":
                        j = 0
                        for lm in hand_landmarks.landmark:
                            self.right["position"][self.HAND_KEYPOINTS[j]] = [lm.x,lm.y, lm.z]
                            j = j + 1
                        self.right["score"] = hand_class.score
                    else:
                        j = 0
                        for lm in hand_landmarks.landmark:
                            self.left["position"] [self.HAND_KEYPOINTS[j]] = [lm.x,lm.y, lm.z]
                            j = j + 1
                        self.left["score"] = hand_class.score

        return self.left, self.right, image_points

    #World Landmarks
    def getWorldLandmarks(self,img):
        """ Get landmarks from hands 
        
        Parameters
        ----------

        img : cv2 image 
            OpenCV image

        Returns
        ----------

        left : dict
            Left hand data
        right : dict
            Right hand data
        """

        # Convert the BGR image to RGB before processing.
        self.results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        img_h, img_w, _ = img.shape 

        self.left = {"position": self.dict_points.copy(), "score":0}
        self.right = {"position": self.dict_points.copy(), "score":0} 
        model_points = None

        if self.results.multi_hand_world_landmarks:
            model_points = self.results.multi_hand_world_landmarks
            for h_id, hand_landmarks in enumerate(self.results.multi_hand_world_landmarks):
                for c_id, hand_class in enumerate(self.results.multi_handedness[h_id].classification):
                    label = hand_class.label
                    if label == "Right":
                        j = 0
                        for lm in hand_landmarks.landmark:
                            self.right["position"][self.HAND_KEYPOINTS[j]] = [lm.x,lm.y, lm.z]
                            j = j + 1
                        self.right["score"] = hand_class.score
                    else:
                        j = 0
                        for lm in hand_landmarks.landmark:
                            self.left["position"] [self.HAND_KEYPOINTS[j]] = [lm.x,lm.y, lm.z]
                            j = j + 1
                        self.left["score"] = hand_class.score

        return self.left, self.right, model_points


    def getHandsInfo(self,img):
        left, right, model_points = self.getWorldLandmarks(img)
        world_landmarks = {"left":left, "right":right}
        left, right, image_points = self.getLandmarks(img)
        landmarks = {"left":left, "right": right}
        vectors = self.getHandVectors()
        angles = self.getAnglesFromVectors()

        return landmarks, world_landmarks, vectors, angles
    

    def getHandVectors(self):

        left_position = self.left["position"]
        right_position = self.right["position"]
        score_l = self.left["score"]
        score_r = self.right["score"]

        self.hand_vectors = {"left":{}, "right":{}} 
        self.hand_vectors_np = {"left":{}, "right":{}} 

        for vector_name, points in self.HAND_VECTORS.items():
            if (score_l>.2):
                self.hand_vectors_np["left"][vector_name] = self.__points2vector(tail = left_position[points[0]], head = left_position[points[1]])
                self.hand_vectors["left"][vector_name] = self.hand_vectors_np["left"][vector_name].tolist()
            if (score_r>.2):
                self.hand_vectors_np["right"][vector_name] = self.__points2vector(tail = right_position[points[0]], head = right_position[points[1]])
                self.hand_vectors["right"][vector_name] = self.hand_vectors_np["right"][vector_name].tolist()

        return self.hand_vectors

    def getAnglesFromVectors(self):


        score_l = self.left["score"]
        score_r = self.right["score"]
        self.hand_angles = {"left":{}, "right":{}} 

        for vector_name, value in self.HAND_JOINTS.items():
            if (score_l>.2):
                vector1 = self.hand_vectors_np["left"][value[0]]
                vector2 = self.hand_vectors_np["left"][value[1]]
                self.hand_angles["left"][vector_name] = self.__getAngle(vector1,vector2)
            
            if (score_r>.2):

                vector1 = self.hand_vectors_np["right"][value[0]]
                vector2 = self.hand_vectors_np["right"][value[1]]
                self.hand_angles["right"][vector_name]= self.__getAngle(vector1,vector2)

        return self.hand_angles

    

    def drawLandmarks(self, img, style=1):
        img_h, img_w, _ = img.shape 

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands 

        if (self.results.multi_hand_landmarks):
            for h_id, hand_landmarks in enumerate(self.results.multi_hand_landmarks):

                if(style==0):
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                else:
                    for line_id in self.landmark_line_ids:
                        lm = hand_landmarks.landmark[line_id[0]]
                        lm_pos1 = (int(lm.x * img_w), int(lm.y * img_h))
                        lm = hand_landmarks.landmark[line_id[1]]
                        lm_pos2 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.line(img, lm_pos1, lm_pos2, (128, 0, 0), 1)

                    # plot circles
                    z_list = [lm.z for lm in hand_landmarks.landmark]
                    z_min = min(z_list)
                    z_max = max(z_list)
                    for lm in hand_landmarks.landmark:
                        lm_pos = (int(lm.x * img_w), int(lm.y * img_h))
                        lm_z = int((lm.z - z_min) / (z_max - z_min) * 255)
                        cv2.circle(img, lm_pos, 3, (255, lm_z, lm_z), -1)

                hand_texts = []
                for c_id, hand_class in enumerate(self.results.multi_handedness[h_id].classification):
                    #hand_texts.append("#%d-%d" % (h_id, c_id)) 
                    hand_texts.append("- Index: %d" % (hand_class.index))
                    hand_texts.append("- Label: %s" % (hand_class.label))
                    #hand_texts.append("- Score:%3.2f" % (hand_class.score * 100))
                lm = hand_landmarks.landmark[0]
                lm_x = int(lm.x * img_w) - 50
                lm_y = int(lm.y * img_h) - 10
                lm_c = (104, 0, 0)
                for cnt, text in enumerate(hand_texts):
                    cv2.putText(img, text, (lm_x, lm_y + 12 * cnt), cv2.FONT_HERSHEY_SIMPLEX, 0.4, lm_c, 2)
            return img
        else:
            cv2.putText(img, "No hands", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 140), 2)
            pass
        return img
    

    def getWorldPoints(self,img, camera_matrix, distortion):
        frame_height, frame_width, channels = img.shape
        world_points = []
        world_points_hand = {'right': {'position': self.dict_points.copy()}, 'left' : {'position': self.dict_points.copy()} }
        self.results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        
        if self.results.multi_hand_landmarks:
            for [i, hand_landmarks] in enumerate(self.results.multi_hand_landmarks):
                world_landmarks = self.results.multi_hand_world_landmarks[i]
                for c_id, hand_class in enumerate(self.results.multi_handedness[i].classification):
                    label = hand_class.label
                        
                    model_points = np.float32([[-l.x, -l.y, -l.z] for l in world_landmarks.landmark])
                    image_points = np.float32([[l.x * frame_width, l.y * frame_height] for l in hand_landmarks.landmark])

                    #Perspective-n-Point
                    success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix, distortion, flags=cv2.SOLVEPNP_SQPNP)

                    transformation = np.eye(4)  # needs to 4x4 because you have to use homogeneous coordinates
                    transformation[0:3, 3] = translation_vector.squeeze()
                    # the transformation consists only of the translation, because the rotation is accounted for in the model coordinates. Take a look at this (https://codepen.io/mediapipe/pen/RwGWYJw to see how the model coordinates behave - the hand rotates, but doesn't translate

                    # transform model coordinates into homogeneous coordinates
                    model_points_hom = np.concatenate((model_points, np.ones((21, 1))), axis=1)

                    # apply the transformation
                    world_points = model_points_hom.dot(np.linalg.inv(transformation).T)

                    j = 0
                    for p in world_points:
                        if(label == 'Right'):
                            world_points_hand['right']["position"][self.HAND_KEYPOINTS[j]] = p
                        else:
                            world_points_hand['left']["position"][self.HAND_KEYPOINTS[j]] = p
                        j += 1



        
        return world_points_hand


"""
# OpenCV code
import cv2
img = cv2.imread('sample.png')

h = MediapipeHand();
landmarks, vectors, angles = h.getHandsInfo(img)

print (vectors)
print (angles)


# Display image with drawing hands

cv2.imshow("Result", h.drawLandmarks(img))
cv2.waitKey(0)
"""

"""
import cv2

h = MediapipeHand()

cap = cv2.VideoCapture(0)  
if cap.isOpened():
    while True:
        success, img = cap.read()
        if not success:
            continue
        else:
            image_points, model_points, vectors, angles = h.getHandsInfo(img)
            world_points = h.getWorldPoints(img)
            #print("Digital landmarks \n")
            #print (image_points,"\n")
            #print("world landmarks \n")
            #print(model_points,"\n")

            print("World points \n")
            print(world_points, "\n")

            cv2.imshow("Result", h.drawLandmarks(img,1))
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break
cap.release()

"""