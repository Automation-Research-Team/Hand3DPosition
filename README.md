# Hand_3DPosition
Get the 3D position of a hand using MediaPipe

**How to use it:**

- Change the path of the .json file in calibration_camera.py, test_hand.py and thinklet.py to a path in your computer.

- Install HXRI and run the commands in the readme inside the folder

  **If you want to use it with laptop webcam:**
  
  - In calibration_camera.py descomment the lines to use the frame from the webcam and comment the NEP+ lines
  - Run calibration_camera.py 
  - Show a chess dashboard to the camera
  - Click 's' with the dashboard in different positions to do the calibration
  - Once you get the parameters run test_hand.py
  
  
  **If you want to use it with Thinklet device:**
  
  - Install NEP+
  - Install chocolatey and scrcpy
  - Connect Thinklet device
  - Run SCRCPY command
  - Click HXRI app
  - Click connect
  - Run Nep master
  - Run test_sub.py
  - Run calibration_camera.py 
  - Show a chess dashboard to the camera
  - Click 's' with the dashboard in different positions to do the calibration
  - Once you get the parameters run thinklet.py
