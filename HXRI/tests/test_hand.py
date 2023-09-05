import hxri.HandDetector
import cv2

h = hxri.HandDetector.MediapipeHand();

cap = cv2.VideoCapture(0)  
if cap.isOpened():
    while True:
        success, img = cap.read()
        if not success:
            continue
        else:
            landmarks, vectors, angles = h.getHandsInfo(img)
            print (landmarks)

            cv2.imshow("Result", h.drawLandmarks(img,1))
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q') or key == 0x1b:
                break
cap.release()
