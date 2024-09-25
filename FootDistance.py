import cv2
import nep
import numpy as np
#import HandDetector
import json
import matplotlib.pyplot as plt


aruco_side = 6.35 #cm

class MovingAverage:
    def __init__(self, size):
        self.size = size
        self.buffer = []
    
    def add(self, value):
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)
        self.buffer.append(value)
        return self.get_average()
    
    def get_average(self):
        if not self.buffer:
            return 0
        return sum(self.buffer) / len(self.buffer)

filter_size = 10
depth_filter = MovingAverage(filter_size)

def nepSubscriber():
    node = nep.node("subscriber_tk")    # Create a new node                    
    sub = node.new_sub("androidCamera", "images")   # Select the configuration of the subscriber
    while True:
        s, msg = sub.listen()       # Non blocking socket
        if s:
            #msg = cv2.flip(msg, 1)
            frame = arucoDetector(msg)

            cv2.imshow("Result", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break

def webcam():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()


    while True:
        ret, frame = cap.read()
        if ret:
            frame = arucoDetector(frame)
            cv2.imshow("Result", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break
    cap.release()


def arucoDetector(frame):
    file = open('cameraDataThinklet.json')
    camera_data = json.load(file)
    camMatrix = np.array(camera_data['matrix'])
    distCoeff = np.array(camera_data['distortion'])

    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)

    
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bboxes, ids, rejected = detector.detectMarkers(frameGray)

    if len(bboxes) > 0:
        rvecs, tvecs, obj_points = cv2.aruco.estimatePoseSingleMarkers(bboxes, aruco_side, camMatrix, distCoeff)

        for bbox, id, tvecs in zip(bboxes, ids, tvecs):
            bbox = bbox[0]
            tvec = tvecs[0]
            if len(bbox) > 0:
                
                for xy in bbox:
                    cv2.circle(frame, (int(xy[0]), int(xy[1])), 5, (0,255,0), cv2.FILLED)
                center_x = (int(sum([x[0] for x in bbox]) / 4))
                center_y = (int(sum([x[1] for x in bbox]) / 4))
                center = [center_x, center_y]
                # print("center:", center)
                z = round(tvec[2], 3)

                filtered_z = depth_filter.add(z)

                cv2.putText(frame, f'Pose ArUco: ({filtered_z:.2f} cm)', (10,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0,0,0),2)
                return frame
    else:
        cv2.putText(frame, "Waiting for ArUco", (10,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,0,255),2)
        return frame



if __name__ == '__main__':
    webcam()
    cv2.destroyAllWindows()



