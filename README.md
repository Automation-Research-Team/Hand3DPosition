# Hand_3DPosition
Get the 3D position of a hand using MediaPipe

# Install python libraries

pip install mediapipe=0.10.3
pip install nep
pip install matplotlib
pip install opencv-python==4.7.0.68


# Installation Guide for Thinklet

Follow the steps below to set up your development environment:

1. **Install Node.js**
   
   Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine. It's necessary for running JavaScript on your machine.

   Download and install Node.js from the official website: [Node.js Download](https://nodejs.org/en)

2. **Install NEP-CLI**

   NEP-CLI is a command line interface for NEP development. It helps in creating, testing, and deploying NEP+ applications.

   Follow the installation guide provided in the official documentation: [NEP-CLI Installation Guide](https://enrique-coronado.gitbook.io/nep-docs/developer-tools/nep-cli#installation)

3. **Install scrcpy**

   Scrcpy is a versatile tool that mirrors Android devices (both video and audio) connected via USB or over TCP/IP. It allows you to control the device using your computer's keyboard and mouse.
   Additionally, scrcpy provides a convenient way to install APK Android applications. Simply copy and paste the required APK onto the scrcpy screen mirroring the Android device.

   For installation instructions and more information, visit the official GitHub repository: [scrcpy on GitHub](https://github.com/Genymobile/scrcpy)

4. **Install HXRI_android.apk using scrcpy**
   HXRI_android is an Android application that allows you to send images from your Android device (in this case, Thinklet) to your computer.
   To install HXRI_android.apk using scrcpy, follow these steps:
   - Ensure your Android device is connected to your computer and scrcpy is running.
   - Locate the HXRI_android.apk file on your computer.
   - Copy the HXRI_android.apk file and paste it onto the scrcpy screen that is mirroring your Android device. The installation process should begin automatically.

5. **Change permissions of HXRI_android.apk to enable camera usage**

   After installing the HXRI_android application, you need to grant it permission to use the camera on your Android device. Follow these steps:
   - On your Android device, go to Settings > Apps & notifications.
   - Find and select the HXRI_android application.
   - Tap on Permissions.
   - Find and toggle on the Camera permission.

  Now, the HXRI_android application should have the necessary permissions to access and use the camera on your Android device.


# Sending Images from Thinklet to the Computer

Follow the steps below to send images from your Thinklet device to your computer:

1. **Start the NEP Master**
   Run the NEP-CLI master command in your terminal:

   `nep master`

2. **Launch the HXRI_android Application**
   Use scrcpy to execute the HXRI_android application on your Thinklet device.

3. **Set the Computer's IP Address**
   The HXRI_android application needs to know the IP address of the computer it will connect to. You can obtain this by running the following NEP-CLI command in your terminal:

   `nep ip`

   Once you have the IP address, enter it into the text field in the HXRI_android application and press the 'Connect' button.

4. **Verify Image Transmission**
   To confirm that the HXRI_android application is successfully sending images to your computer, run the following command in your terminal:
   `nep show androidCamera images`

   This will open a new window in your default web browser, displaying the images transmitted from the Thinklet device.

5. **Camera Calibration**
   Follow the steps below to calibrate your camera:
   - Execute the `CalibrationCamera.py` script. This script initiates the calibration process.
   - Present a chessboard pattern to the camera. This pattern helps the calibration algorithm determine lens distortions.
   - Press the 's' key while holding the chessboard in various positions and orientations. Each press captures a snapshot for the calibration process.

     Note: Ensure the chessboard fills a significant portion of the frame in each snapshot and that the pattern is clearly visible.

6. **Obtain 3D Positions Using MediaPipe**
   After successfully acquiring the necessary parameters, execute the `Thinklet.py` script. This script utilizes the MediaPipe framework to compute and output 3D positions from the input data.


#   Use with laptop webcam:
  
  - In `CalibrationCamera.py` descomment the lines to use the frame from the webcam and comment the NEP+ lines
  - Run `CalibrationCamera.py`
  - Show a chess dashboard to the camera
  - Click 's' with the dashboard in different positions to do the calibration
  - Once you get the parameters run `TestWebcam.py`
  
  
