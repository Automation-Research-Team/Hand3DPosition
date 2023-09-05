import hxri.HandDetector
import cv2
import threading

import nep
import time
import sys


node_name = "hxri/mediapipe/script"
node = nep.node(node_name)             
sub_signal = node.new_sub("hxri/parameter", "json") 
sub_syncro = node.new_sub("hxri/signal/syncro", "json")    
pub_state = node.new_pub("hxri/state", "json")


#try:
    #print (sys.argv)
    #topic = sys.argv[1]
    #print("Topic:" + topic)
    #sys.stdout.flush()

#except Exception as e:
    #print(e, file=sys.stderr)


pub_hands = node.new_pub("nepplus/mediapipe/hands","json") 

n_cameras = 1
cameras = {1:{},2:{},3:{}}
running = True

def run(camera):
        global cameras, running
        cap = cv2.VideoCapture(cameras[camera]["camera_index"])  
        if cap.isOpened():
                while running:
                        success, cameras[camera]["image"] = cap.read()
                        if success:
                                cv2.imshow(str(camera),cameras[camera]["image"])
                                key = cv2.waitKey(1) & 0xFF
                                if key == ord('q') or key == ord('Q') or key == 0x1b:
                                        break

        cap.release()

def hands(camera):
        global cameras, running
        h = hxri.HandDetector.MediapipeHand();
        while running:
                if cameras[camera]["detect"]["hands"] == True:
                        try:
                                # Code ----------------------
                                landmarks, vectors, angles = h.getHandsInfo(cameras[camera]["image"])
                                pub_hands.publish ({cameras[camera]["id"]:{"hand_landmarks":landmarks}})
                                # ---------------------------
                                cv2.imshow("hands", h.drawLandmarks(cameras[camera]["image"]))
                                key = cv2.waitKey(1) & 0xFF
                                if key == ord('q') or key == ord('Q') or key == 0x1b:
                                        break
                        except:
                                pass
 
for n in range(n_cameras):
        th_image = threading.Thread(target=run, args=(n,))
        th_hands = threading.Thread(target=hands, args=(n,))
        cameras[n] = {"th_hands":th_hands,"th_image":th_image, "detect":{"hands":True}, "id":n, "camera_index":n, "image":""}
        th_image.start()
        th_hands.start()





def run2(camera):
        global cameras, running
        h = hxri.HandDetector.MediapipeHand();
        cap = cv2.VideoCapture(cameras[camera]["camera_index"])  
        if cap.isOpened():
                while running:
                        success, img = cap.read()
                        if success:
                                if cameras[camera]["detect"]["hands"] == True:
                                        # Code ----------------------
                                        landmarks, vectors, angles = h.getHandsInfo(img)
                                        pub_hands.publish ({cameras[camera]["id"]:{"hand_landmarks":landmarks}})
                                        # ---------------------------
                                        cv2.imshow(str(camera), h.drawLandmarks(img))
                                        key = cv2.waitKey(1) & 0xFF
                                        if key == ord('q') or key == ord('Q') or key == 0x1b:
                                                break
        cap.release()


        cap.release()



while running:
        s, value = sub_signal.listen()
        if s:
                print(value)
                if(node_name in value):
                        msg = value[node_name]
                        if("hands_on" in msg):
                                hands_on[camera] = msg["hands_on"]
                        if("skeleton_on" in msg):
                                skeleton_on[camera] = msg["skeleton_on"] 
                        if("face_on"[camera] in msg):
                                face_on = msg["face_on"] 
                        if("close" in msg):
                                running =  False
                                time.sleep(.5)
        else:
                time.sleep(.001)
