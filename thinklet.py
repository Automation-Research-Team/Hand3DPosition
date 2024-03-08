import cv2
import nep
import numpy as np
import hxri.HandDetector
import json
import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure()
ax = plt.axes(projection ='3d')

#store the coordinates of the hand in an array
def getHandPoints(world_points, label):
    global fig, ax
    x = []
    y = []
    z = []
    for k in world_points[label]['position']:
                    pose = world_points[label]['position'][k]
                    x.append(pose[0]*-1)
                    y.append(pose[1])
                    z.append(pose[2])

    #Draw the figure of the hand
    ax.plot(x[0:5],y[0:5],z[0:5])
    for i in range(0,4):
         ax.plot(x[5+(i*4):9+(i*4)],y[5+(i*4):9+(i*4)],z[5+(i*4):9+(i*4)])

    ax.plot([x[0],x[5],x[9],x[13],x[17],x[0]],[y[0],y[5],y[9],y[13],y[17],y[0]],[z[0],z[5],z[9],z[13],z[17],z[0]])    
    # Add the camera coordinate
    ax.scatter(0,0,0)
    ax.scatter(x, y, z)

#Plot the hand points detected in the real world
def plotHand(world_points):
    global fig, ax
    
    try:
        getHandPoints(world_points,'left')
    except:
         pass
    try:
        getHandPoints(world_points,'right')
    except:
         pass
    # plotting
    ax.scatter(0,0,0)
    ax.set_title('Hands')
    plt.show(block=False)
    plt.pause(0.0001)
    ax.cla()

#Load the camera information from a json file
file = open('cameraData.json')
camera_data = json.load(file)

node = nep.node("subscriber_tk")    # Create a new node                    
h = hxri.HandDetector.MediapipeHand()
sub = node.new_sub("androidCamera", "image")   # Select the configuration of the subscriber
while True:
    s, msg = sub.listen()       # Non blocking socket
    if s:                       # Info avaliable only if s == True
        msg = cv2.flip(msg,1)  
        #landmarks, vectors, angles = h.getHandsInfo(msg)
        
        #Get camera parameters
        mtx =np.array(camera_data['matrix'])
        distortion = np.array(camera_data['distortion'])
        image_points, model_points, vectors, angles = h.getHandsInfo(msg)

        #Get World points in meters
        world_points = h.getWorldPoints(msg,mtx,distortion)
        try:
            #plot world_points and print coordinates
            plotHand(world_points)
            print(world_points)
        except:
            print('No hand')

        #show the frame with landmarks 
        cv2.imshow("Result", h.drawLandmarks(msg,1))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q') or key == 0x1b:
            break
        




