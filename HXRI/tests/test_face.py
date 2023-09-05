import hxri.FaceDetector
import cv2
h = hxri.FaceDetector.MediapipeFace();

cap = cv2.VideoCapture(0)  
if cap.isOpened():
    while True:
        success, img = cap.read()
        if not success:
            continue
        # Code ----------------------
        data = h.getFace(img)
        img = h.drawFace(img)
        # ---------------------------

        cv2.imshow("Result", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q') or key == 0x1b:
            break

cap.release()
