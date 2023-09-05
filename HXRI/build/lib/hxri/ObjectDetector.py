import os
os.environ['PATH'] = 'C:/nep/opencv_cuda' + os.pathsep + os.environ['PATH']
import cv2
import numpy as np

class SSD():
    import numpy as np
    import time

    def __init__(self, classes, path_deep_model, config = {"inpWidth":320,"inpHeight":320,"confThreshold":0.5}, fix_index = False):
        self.classes = classes
        self.config = config
        self.fix_index = fix_index
        self.confThreshold = config["confThreshold"]

        print("[INFO] Loading model...")

        self.net = cv2.dnn.readNetFromCaffe(path_deep_model + "/model.prototxt",  path_deep_model +  "/model.caffemodel")
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        print("[INFO] Model ready...")

    def getObjects(self,img):
        # Runs the detection on a frame and return bounding boxes and predicted labels
        detections = self.predict_detection(img, self.net)
        self.detected = self.proccess_prediction(img, detections, self.confThreshold)
        return self.detected

    def drawObjects(self, img_src):

        new_image = img_src.copy()

        for value in self.detected: 
            startX = value["box"]["x"] 
            startY = value["box"]["y"] 
            endX = startX + value["box"]["w"] 
            endY = startY + value["box"]["h"]
            cv2.rectangle(new_image, (startX, startY), (endX, endY),(255, 0, 0), 2)
            labelPosition = endY - 5
            cv2.putText(new_image, value["label"], (startX, labelPosition),
                    cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)

        # Put efficiency information. The function getPerfProfile returns the 
        # overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = self.net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        cv2.putText(new_image, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        return new_image



    def predict_detection(self,frame, net):
        '''
        Predict the objects present on the frame
        '''
        # Conversion to blob
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)
        #blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), (127.5, 127.5, 127.5), False)
        # Detection and prediction with model
        self.net.setInput(blob)
        return self.net.forward()


    def proccess_prediction(self, frame, detections, threshold):
        '''
        Filters the predictions with a confidence threshold and draws these predictions
        '''

        detected = []
        (height, width) = frame.shape[:2]
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
        
            if confidence > threshold:
                # Index of class label and bounding box are extracted
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])

                # Retreives corners of the bounding box
                (startX, startY, endX, endY) = box.astype("int")
                label_ = "{}: {:.2f}%".format(self.classes[idx], confidence*100)
                label = self.classes[idx]
                position = [(startX + endX)/2, (startY + endY)/2]
                w = endX - startX
                h = endY - startY

                detected.append({"label":label, "center":{"x":int(position[0]), "y":int(position[1])},  "box":{"x":int(startX), "y":int(startY), "w":int(w), "h":int(h)}, "confidence":float(confidence)})

        return detected


class YOLO():

    import numpy as np
    import time


    def __init__(self, classes, path_deep_model, config = {"inpWidth":320,"inpHeight":320,"confThreshold":0.5, "nmsThreshold":0.5},  use_gpu = False, fix_index = False):
        self.classes = classes
        self.config = config
        self.fix_index = fix_index
        self.confThreshold = config["confThreshold"]
        self.nmsThreshold =  config["nmsThreshold"]

        print("[INFO] Loading model...")

        modelConfiguration = path_deep_model + "/model.cfg";
        modelWeights = path_deep_model + "/model.weights";

        self.net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        if use_gpu:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
            print("[INFO] Using GPU...")
        else:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) # DNN_TARGET_OPENCL_FP16,DNN_TARGET_OPENCL,DNN_TARGET_CPU = 0
            print("[INFO] Using CPU...")

        print("[INFO] DL model ready...")


    def _getOutputsNames(self, net):
        # Get the names of all the layers in the network
        layersNames = net.getLayerNames()
        if(self.fix_index == True):
            # Get the names of the output layers, i.e. the layers with unconnected outputs
            return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        else:
            # Get the names of the output layers, i.e. the layers with unconnected outputs
            return [layersNames[i-1] for i in net.getUnconnectedOutLayers()]

    # Remove the bounding boxes with  low confidence using non-maxima suppression
    def _postprocess(self, frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        #list_labels = []
        #list_index = []
        detected = []


        for i in indices:
            index = i
            try:
                index = i[0]
            except:
                index = i
                pass
            box = boxes[index]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]

            if confidences[index] > 0.5:
                label = self.classes[classIds[index]]
                position = [left + width/2, top + height/2]
                #list_index.append(classIds[i])
                #list_labels.append(label)
                detected.append({"label":label,"center":{"x":int(position[0]), "y":int(position[1])}, "box":{"x":left, "y":top, "w":width, "h":height}, "confidence":confidences[index]})
        return detected

    def drawObjects(self, img_src):

        new_image = img_src.copy()

        for value in self.detected: 
            startX = value["box"]["x"] 
            startY = value["box"]["y"] 
            endX = startX + value["box"]["w"] 
            endY = startY + value["box"]["h"]
            cv2.rectangle(new_image, (startX, startY), (endX, endY),(255, 0, 0), 2)
            labelPosition = endY - 5
            cv2.putText(new_image, value["label"], (startX, labelPosition),
                    cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)

        # Put efficiency information. The function getPerfProfile returns the 
        # overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = self.net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        cv2.putText(new_image, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        return new_image
    
    def getObjects(self, img):

        blob = cv2.dnn.blobFromImage(img, 1/255, (self.config["inpWidth"], self.config["inpHeight"]), [0,0,0], 1, crop=False)
        
        # Sets the input to the network
        self.net.setInput(blob)
        
        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self._getOutputsNames(self.net))
     
        # Remove the bounding boxes with low confidence
        self.detected = self._postprocess(img, outs)

        return self.detected

