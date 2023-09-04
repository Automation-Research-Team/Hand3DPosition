import cv2
import nep
import base64
import numpy as np


sub_type = "normal"                 # Type of subscriber. "callback" or "normal"
msg_type = "string"                   # Message type to listen. "string" or "dict"

node = nep.node("subscriber_sample")                                                        # Create a new node
conf = node.direct(ip = "192.168.50.133", port =  9090, mode ="one2many")                         # Select the configuration of the subscriber

pub = node.new_pub("test", "image");
def callback(msg):
    print ("Callback get")
    print (msg)

if sub_type == "normal":            # Listen info inside a while loop
    sub = node.new_sub("test", msg_type, conf) 
    while True:
        s, msg = sub.listen()       # Non blocking socket
        if s:                       # Info avaliable only if s == True
            
            #print(msg)
            jpg = base64.b64decode(msg)
            jpg = np.frombuffer(jpg, dtype=np.uint8)
            img = cv2.imdecode(jpg, 1)
            pub.publish(img)



