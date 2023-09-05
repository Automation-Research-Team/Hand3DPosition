import hxri.BodyDetector
import cv2

import nep
import time
import sys

msg_type = "json"         # Message type to listen. "string" or "json"

node = nep.node("publisher_sample")             # Create a new node
pub = node.new_pub("HumanBody",msg_type)        # Set the topic and the configuration of the publisher





h = hxri.BodyDetector.MediapipeBody();

cap = cv2.VideoCapture(0)  
if cap.isOpened():
    while True:
        success, img = cap.read()
        if not success:
            continue
        # Code ----------------------
        landmarks, vectors, angles = h.getBodyInfo(img)
        h.getAnglesFromVectors()
        pub.publish(angles) 
        print (angles)
        # ---------------------------

        cv2.imshow("Result", h.drawLandmarks(img))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q') or key == 0x1b:
            break

cap.release()
