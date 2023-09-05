import hxri.ObjectDetector
import cv2

# Relevant code --------------------------
def getClasses(path_deep_model):
    classes = None
    classesFile = path_deep_model + "/model.names"
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    print(classes)
    return classes

# Example of a folder with the required files
path_deep_model = 'C:/nep/deep_models/objects/mobilenet-ssd'
classes =  getClasses(path_deep_model)

y = hxri.ObjectDetector.SSD(classes, path_deep_model);

#-----------------------------------------

import cv2  
import numpy as np

cap = cv2.VideoCapture(0)   
if cap.isOpened():
    while True:
        success, img = cap.read()
        if not success:
            continue


    
        # Relevant code --------------------------
        data = y.getObjects(img)
        img = y.drawObjects(img)
        #-----------------------------------------

        #print(data)
        cv2.imshow("Result", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q') or key == 0x1b:
            break

cap.release()

