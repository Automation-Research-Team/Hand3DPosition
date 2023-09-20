import hxri.HandDetector
import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
import time

#Create the HandDetector object
h = hxri.HandDetector.MediapipeHand()

file = open('C:/Users/andreas/Documents/GitHub/Hand_3DPosition/cameraData.json')
camera_data = json.load(file) #Charge the camera mtx and distortion from json file

#variables to plot
plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(projection ='3d')
ax2 = fig.add_subplot(projection ='3d')
ax2.axes.set_xlim3d(left=-4, right=4)
ax2.axes.set_ylim3d(bottom=-4, top=4) 
ax2.axes.set_zlim3d(bottom=-4, top=4) 

def getHandPoints(world_points, label, id):
    global ax1, ax2
    x = []
    y = []
    z = []
    #Get the x,y,z coordinates and store them in arrays
    for k in world_points[label]['position']:
                    pose = world_points[label]['position'][k]
                    x.append(pose[0]*-1)
                    z.append(pose[1])
                    y.append(pose[2])
    
    #Unite the points to create the hand figure
    if (id == 1): 
        ax1.plot(x[0:5],y[0:5],z[0:5])
    else:
         ax2.plot(x[0:5],y[0:5],z[0:5])
    
    for i in range(0,4):
        if(id == 1):
            ax1.plot(x[5+(i*4):9+(i*4)],y[5+(i*4):9+(i*4)],z[5+(i*4):9+(i*4)])
        else:
            ax2.plot(x[5+(i*4):9+(i*4)],y[5+(i*4):9+(i*4)],z[5+(i*4):9+(i*4)])
        
    if(id == 1):
        ax1.plot([x[0],x[5],x[9],x[13],x[17],x[0]],[y[0],y[5],y[9],y[13],y[17],y[0]],[z[0],z[5],z[9],z[13],z[17],z[0]])    
        # plotting
        ax1.scatter(x, y, z)
    else:
        ax2.plot([x[0],x[5],x[9],x[13],x[17],x[0]],[y[0],y[5],y[9],y[13],y[17],y[0]],[z[0],z[5],z[9],z[13],z[17],z[0]])    
        # plotting
        ax2.scatter(x, y, z)

#Plot the hand points detected 
def plotHand(world_points, id):
    global ax1, ax2
    if(id == 1):
        ax1.cla()
        #update points, and try to check if there is left or right hand
        try:
            getHandPoints(world_points,'left', id)
        except:
            pass
        try:
            getHandPoints(world_points,'right',id)
        except:
            pass
        # plotting
        ax1.scatter(0,0,0)
        ax1.set_title('point model')
    else:
        ax2.cla()
        try:
            getHandPoints(world_points,'left', id)
        except:
            pass
        try:
            getHandPoints(world_points,'right',id)
        except:
            pass
        # plotting
        ax2.scatter(0,0,0)
        # ax2.scatter(-0.4,-0.4,-0.1)
        # ax2.scatter(-0.4,-0.4,0.1)
        # ax2.scatter(0.4,-0.4,-0.1)
        # ax2.scatter(0.4,-0.4,0.1)
        ax2.set_title('world model') 
    plt.show(block=False)
    plt.pause(0.0001)


cap = cv2.VideoCapture(0)  
if cap.isOpened():
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        if not success:
            continue
        else:
            #Get the matrix and distortion from the camera and use it to get the world points
            mtx =np.array(camera_data['matrix'])
            distortion = np.array(camera_data['distortion'])
            image_points, model_points, vectors, angles = h.getHandsInfo(img)
            world_points = h.getWorldPoints(img,mtx, distortion)

            #plotHand(model_points, 1)
            print(image_points)
            plotHand(world_points, 2)

            cv2.imshow("Result", h.drawLandmarks(img,1))
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break
cap.release()