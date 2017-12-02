import cv2
import numpy as np
import argparse
from os.path import join
import os

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
    default = '20171129_163535.mp4',
	help="path to input video")
    ap.add_argument("-p", "--prototxt", type=str,
    default=join(os.getcwd(), 'MobileNetSSD_deploy.prototxt'),
	help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", type=str,
    default=join(os.getcwd(), 'MobileNetSSD_deploy.caffemodel'),
	help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")

    return vars(ap.parse_args())

opts = get_args()

cap = cv2.VideoCapture(opts['video'])
net = cv2.dnn.readNetFromCaffe(opts['prototxt'], opts['model'])

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"] ## 15
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
n_frame = 0
last_found = 0
while(True):
    ret, frame = cap.read()
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
    (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > opts['confidence']:
            idx = int(detections[0, 0, i, 1])
            if idx == 15:
                last_found = n_frame
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                print("[INFO] {} missed frames: {}".format(label, n_frame - last_found))
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    cv2.imshow("output", cv2.resize(frame, (300, 300)))
    n_frame +=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
