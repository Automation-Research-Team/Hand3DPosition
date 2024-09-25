import dis
import numpy as np
import cv2 as cv
import glob
import json
import nep

square_size = 4.5 #cm

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((5*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:5].T.reshape(-1,2)
objp = objp*square_size
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
cont = 0

camera_data = {'matrix' : None, 'distortion' :None }


node = nep.node("subscriber_tk")    # Create a new node                    
sub = node.new_sub("androidCamera", "images")   # Select the configuration of the subscriber

imgs = []

# cap = cv.VideoCapture(0)  
# if cap.isOpened():

while True:
    # s , msg = cap.read()
    s, msg = sub.listen()       # Non blocking socket
    if s:
        msg = cv.flip(msg,1)                       # Info avaliable only if s == True
        gray = cv.cvtColor(msg, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (7,5), None)
        # If found, add object points, image points (after refining them)

        key = cv.waitKey(1) & 0xFF
        if ret == True:
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            #Save the chess board image if s is pressed
            if key == ord('s') or key == ord('S'):
                objpoints.append(objp)
                imgpoints.append(corners2)
                print("Imagen num: ", cont)
                cont+=1
            
            # Draw and display the corners
            cv.drawChessboardCorners(msg, (7,5), corners2, ret)
        cv.imshow('img', msg)
        key = cv.waitKey(1) & 0xFF

        if key == ord('q') or key == ord('Q') or key == 0x1b or cont == 10:
            break
            
#Get the distotion vector and mtrx of the camera
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

mtx = mtx.tolist()
dist = dist.tolist()

#Put the data in a dict
camera_data['matrix'] = mtx
camera_data['distortion'] = dist

json.JSONEncoder().encode(camera_data)

#Save the data in a file, change this path to one in your own computer
with open('C:/Users/jchr2003/Desktop/Hand3DPosition-main/cameraDataNew.json', 'w') as outfile:
    json.dump(camera_data,outfile)
#Announce when data are saved
print("Data saved \n")
cv.destroyAllWindows()
