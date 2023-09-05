import os
os.environ['PATH'] = 'C:/nep/opencv_cuda' + os.pathsep + os.environ['PATH']
import cv2
import numpy as np
import math


class MediapipeFace():

    def __init__(self, model_selection=1, min_detection_confidence=0.5):
        import mediapipe as mp
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_detection = mp.solutions.face_detection

        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=model_selection, min_detection_confidence=min_detection_confidence)


    def _normalized_to_pixel_coordinates(self, normalized_x, normalized_y, image_width,image_height):

        x_px = min(math.floor(normalized_x * image_width), image_width - 1)
        y_px = min(math.floor(normalized_y * image_height), image_height - 1)
        
        return x_px, y_px

    def drawFace(self, image_src):

        if len(self.faces) == 0:
            return image_src            
        else:
            new_image = image_src.copy()
            for detection in self.face_results.detections:
                self.mp_drawing.draw_detection(new_image, detection)
            return new_image

    def getFace(self, image_src):

            image_src.flags.writeable = False
            image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2RGB)
            self.face_results = self.face_detection.process(image_src)
            y_resolution, x_resolution, c = image_src.shape
            image_src.flags.writeable = True

            self.faces = {}
            if self.face_results.detections:
                for detection in self.face_results.detections:
                    data = detection.location_data
                    xmin = data.relative_bounding_box.xmin
                    ymin = data.relative_bounding_box.ymin
                    width = data.relative_bounding_box.width
                    height= data.relative_bounding_box.height
                    xmin, ymin = self._normalized_to_pixel_coordinates(xmin, ymin, x_resolution,y_resolution)
                    width, height = self._normalized_to_pixel_coordinates(width, height, x_resolution,y_resolution)

                    self.faces= {detection.label_id[0]:{"xmin":xmin, "ymin":ymin, "width":width, "height":height}}

                    #print(detection.label_id[0])
                    #print(data.relative_bounding_box.xmin)

                return self.faces