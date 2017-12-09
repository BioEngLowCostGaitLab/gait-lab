from __future__ import print_function
import cv2
import numpy as np
import argparse
from os.path import join
import os

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
    default = join(os.getcwd(), 'resources', '20171129_163535.mp4'),
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
    # args: network, frame, number of passed frames, number of frame in which person was last found, opts
    # returns: frame with rectangle drawn on it, number of frame in which person was last found
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
    (300, 300), 127.5)
    found = False
    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > opts['confidence']:
            idx = int(detections[0, 0, i, 1])
            if idx == 15: # person detected
                found = True
                conf_f = confidence
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                print('[INFO] p: %.2f%% missed frames: %d' %
                (confidence * 100, n_frame - last_found - 1))
                #cv2.rectangle(frame, (startX, startY), (endX, endY),
                #LINECOLOR, 30)
                last_found = n_frame
    if found:
        return startX, startY, endX, endY, last_found, conf_f
    else:
        return 0, 0, 0, 0, 0, 0

def filter_kp(kp, startX, startY, endX, endY, w):
    # filtering criteria: must be smaller than maximum diameter, must be inside rectangle specified by net
    max_size = w * 0.015 # maximum diameter of keypoint
    filtered = []
    for i in range(len(kp)):
        if not (kp[i].size > max_size or kp[i].pt[0] > endX or kp[i].pt[1] > endY or kp[i].pt[0] < startX or kp[i].pt[1] < startY):
            # filtering criteria met
            filtered.append(kp[i])
    return filtered





opts = get_args()

cap = cv2.VideoCapture(opts['video'])
net = cv2.dnn.readNetFromCaffe(opts['prototxt'], opts['model'])
surf = cv2.xfeatures2d.SURF_create(10000)
surf.setUpright(True) # we dont need blob orientation

n_frame = 0
last_found = 0

while(True):
    ret, frame = cap.read()
    grey_frame = cv2.equalizeHist(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.uint8))
    (h, w) = frame.shape[:2]
    if n_frame > 900:
        kp, des = surf.detectAndCompute(grey_frame, None)
        startX, startY, endX, endY, last_found, confidence = evaluate_net(net, frame, n_frame, last_found, opts)
        #if confidence > opts['confidence']:
            #kp = filter_kp(kp, startX, startY, endX, endY, w)
        grey_frame = cv2.drawKeypoints(grey_frame,kp,None,(255,0,0),4)
    cv2.imshow("output", cv2.resize(grey_frame, (640, 360)))
    n_frame +=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
