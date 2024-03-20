
# import libraries
import cv2
import numpy as np
import os
from minio import Minio
from minio.error import S3Error
from datetime import datetime

def upload_image_to_minio(name):
    client = Minio(
        "play.min.io",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        )
    found = client.bucket_exists("cloudcomputing")
    if not found:
        client.make_bucket("cloudcomputing")
    else:
        print("Bucket 'cloudcomputing' already exists")
    b_name = "cloudcomputing"
    o_name = name
    f_name = os.path.join('/home/pi/RatDeduction/Rat',name)
    c_type = "image/jpg"
    client.fput_object(b_name,o_name,f_name,c_type)
    print('File uploaded to MinIo')
        
    


weight = r"yolov4-tiny-custom_final.weights"
cfg = r"yolov4-tiny-custom.cfg"

# give the configuration and weight files for the model and load the network
yolo = cv2.dnn.readNet(cfg, weight)

with open("classes.names", 'r') as f:
    classes = f.read().splitlines()
    
# object to be detected
obj = 'rat'
# find the id of the object to be detected    
id1 = 0

classes = None

with open("classes.names", 'r') as f:
         classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id]) + str(" ") + str(confidence)

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_DUPLEX, 2, color, 2)
    
    cv2.imshow('frame', img)

def imgRead(image):
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open("classes.names", 'r') as f:
         classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet(weight, cfg)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
               center_x = int(detection[0] * Width)
               center_y = int(detection[1] * Height)
               w = int(detection[2] * Width)
               h = int(detection[3] * Height)
               x = center_x - w / 2
               y = center_y - h / 2
               class_ids.append(class_id)
               confidences.append(float(confidence))
               boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        try:
           box = boxes[i]
        except:
             i = i[0]
             box = boxes[i]
    
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
        name = "Rat-detection{}.jpg".format(str(datetime.now()))
        cv2.imwrite(os.path.join('/home/pi/RatDeduction/Rat',name), image)
        print('Rat deducted')
        upload_image_to_minio(name)

        
                
# capture the webcam feed
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('/home/pi/RatDeduction/Rat.mp4')

while(True):
    # read the camera frame
    ret, image = cap.read()
    starttime = datetime.now()
    print('Image captured from frame ' + str(starttime))
    endtime = datetime.now()
    difftime = (endtime - starttime).total_seconds()
    print('Model ran for the captured frame at  ' + str(difftime))
    out = imgRead(image)
    
    

    if cv2.waitKey(1) == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()  

                    
                    
