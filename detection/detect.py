from __future__ import print_function
import cv2
import numpy as np
import argparse
from os.path import join
import os

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
    default = join('resources', '20171129_163535.mp4'),
	help="path to input video")
    ap.add_argument("-p", "--prototxt", type=str,
    default=join(os.getcwd(), 'resources', 'MobileNetSSD_deploy.prototxt'),
	help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", type=str,
    default=join(os.getcwd(), 'resources', 'MobileNetSSD_deploy.caffemodel'),
	help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")

    return vars(ap.parse_args())

def evaluate_net(net, frame, n_frame, last_found, opts):
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
    (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > opts['confidence']:
            idx = int(detections[0, 0, i, 1])
            if idx == 15: # person detected
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                print('[INFO] p: %.2f%% missed frames: %d' %
                (confidence * 100, n_frame - last_found - 1))
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                LINECOLOR, 10)
                last_found = n_frame
    return frame, last_found

opts = get_args()

cap = cv2.VideoCapture(opts['video'])
net = cv2.dnn.readNetFromCaffe(opts['prototxt'], opts['model'])

LINECOLOR = np.array([0, 0, 255])
n_frame = 0
last_found = 0

while(True):
    ret, frame = cap.read()
    (h, w) = frame.shape[:2]
    if n_frame > 1000:
        frame, last_found = evaluate_net(net, frame, n_frame, last_found, opts)

    cv2.imshow("output", cv2.resize(frame, (640, 360)))
    n_frame +=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
