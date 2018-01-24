"""
    NOTE: you need python 2.7, opencv-contrib-python and numpy.
    install python from https://www.python.org/downloads/release/python-2714/
    select to add python to your path variable and to install pip

    Install numpy and opencv-contrib-python:
        "pip install numpy"
        "pip install opencv-contrib-python"
"""

from __future__ import print_function
import cv2
import numpy as np
import argparse
from os.path import join
import os

MIN_BLOBS = 10
MAX_BLOBS = 10

def get_args():
    # user defined arguments, video file in onedrive, ask Antti
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
    default = join(os.getcwd(), 'resources', '20180118_150839.mp4'),
	help="path to input video")
    ap.add_argument("-p", "--prototxt", type=str,
    default=join(os.getcwd(), 'resources', 'MobileNetSSD_deploy.prototxt'),
	help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", type=str,
    default=join(os.getcwd(), 'resources', 'MobileNetSSD_deploy.caffemodel'),
	help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.3,
	help="minimum probability to filter weak detections")
    ap.add_argument("-r", "--rec", type=bool, default=True,
	help="option to draw rectangle")
    ap.add_argument("-f", "--freq", type=int, default=30,
	help="number of images to show per 1 second of footage")
    ap.add_argument("-s", "--save", type=bool, default=False,
	help="option to save detected keypoints")
    ap.add_argument("-d", "--dir", type=str, default=join(os.getcwd(), 'saved_images'),
	help="directory to save detected keypoints")


    return vars(ap.parse_args())

def evaluate_ssd(ssd, frame, n_frame, last_found, opts, startX, startY, endX, endY):
    # args: network, frame, number of passed frames, number of frame in which person was last found, opts
    # returns: top left corner and bottom right corner of rectangle in which person lies,
    # number of frame in which person was last found
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
    (300, 300), 127.5)
    found = False
    ssd.setInput(blob)
    detections = ssd.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > opts['confidence']:
            idx = int(detections[0, 0, i, 1])
            if idx == 15: # person detected
                found = True
                conf_f = confidence
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                print('[INFO] p: %.2f%%' %
                (confidence * 100))
                last_found = n_frame
    if found:
        return startX, startY, endX, endY, last_found, conf_f
    else:
        return startX, startY, endX, endY, last_found, 0

def evaluate_classifier(classifier, kp, frame):
    images = get_keypoint_images(kp, frame)
    input = cv2.dnn.blobFromImages(images)
    classifier.setInput(input)
    output = classifier.forward()
    return output

def overlap(p1, p2):
    # return True if two keypoints overlap
    distance = np.sqrt((p1.pt[0] - p2.pt[0]) ** 2 + (p1.pt[1] - p2.pt[1]) ** 2)
    if distance < p1.size or distance < p2.size:
        return True
    else:
        return False

def delete_overlap(kp):
    # delete overlapping keypoints from list
    # preserve the keypoint with higher response (better keypoint)
    filtered = []

    for i in range(len(kp)):
        for j in range(i + 1, len(kp)):
            if overlap(kp[i], kp[j]):
                if kp[i].response > kp[j].response:
                    kp[j].response = 0
                else:
                    kp[i].response = 0
    for i in range(len(kp)):
        if kp[i].response > 0:
            filtered.append(kp[i])

    return filtered

def filter_kp(kp, h, w):
    # filtering criteria: must be smaller than maximum diameter
    max_size = w * 0.05  # maximum diameter of keypoint
    filtered = []

    for i in range(len(kp)):
        if kp[i].size < max_size and kp[i].pt[1] > 0.3 * h :
            # filtering criteria met
            filtered.append(kp[i])

    for i in range(len(filtered)):
        # move the keypoint to match their location in the image
        filtered[i].pt = (filtered[i].pt[0] + startX, filtered[i].pt[1])

    filtered = delete_overlap(filtered)
    return filtered

def save_keypoints(kp, frame, n_frame, opts):
    # save detected keypoints as 32x32 images
    print('[INFO] saving images')
    for i, keypoint in enumerate(kp):
        final_image = frame[int(keypoint.pt[1]) - 12:int(keypoint.pt[1]) + 12,
                            int(keypoint.pt[0]) - 12:int(keypoint.pt[0]) + 12]
        cv2.imwrite(join(opts['dir'], '%s_%d_%d.png' % (opts['video'].split('\\')[-1], n_frame, i)), final_image)

def get_keypoint_images(kp, frame):
    out = []
    for i, keypoint in enumerate(kp):
        image = frame[int(keypoint.pt[1]) - 12:int(keypoint.pt[1]) + 12,
                            int(keypoint.pt[0]) - 12:int(keypoint.pt[0]) + 12]
        out.append(image)
    return out

def separate(preds, kp):
    markers = []
    ghosts = []
    for i in range(len(preds)):
        if preds[i] > 0.5:
            markers.append(kp[i])
        else:
            ghosts.append(kp[i])
    print(len(markers))
    return markers, ghosts







opts = get_args() # argument list
if opts['freq'] > 60:
    opts['freq'] = 60

cap = cv2.VideoCapture(opts['video'])
ssd = cv2.dnn.readNetFromCaffe(opts['prototxt'], opts['model']) # SSD person detector
classifier = cv2.dnn.readNetFromTensorflow(join(os.getcwd(), 'frozen_model.pb')) # blob classifier



detector = cv2.xfeatures2d.SURF_create(1) # SURF feature detector
detector.setUpright(True) # we dont need blob orientation
n_frame = 0
last_found = 0

if opts['save'] == True:
    try:
        os.mkdir(opts['dir'])
    except:
        pass
startX, startY, endX, endY = 0, 0, 0, 0
while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    frame = cv2.flip(frame, 0)
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.uint8)
    (h, w) = frame.shape[:2]
    if n_frame > 100 and n_frame % (60 / opts['freq']) == 0: # because for now first 800 frames are not interesting
                                                             # also analyse only opts['freq'] frames per second of video
        startX, startY, endX, endY, last_found, confidence = evaluate_ssd(ssd, frame, n_frame, last_found, opts, startX, startY, endX, endY)
        startX, endX = startX - int(0.1 * (endX - startX)), endX + int(0.1 * (endX - startX))
        if (endX > w):
            endX = w
        if True:
            grey_frame = grey_frame[:, startX:endX]
            #grey_frame = cv2.filter2D(grey_frame, -1, kernel)
            while True:
                # adaptive filtering:
                # we want to find between 5-10 blobs in this particular video (2-4 times the actual number of markers visible)
                # the detection threshold of the SURF detector is adjusted according to that withing reasonable range
                kp = detector.detect(grey_frame, None)
                kp = filter_kp(kp, h, w)
                if len(kp) >= MAX_BLOBS:
                    kp = kp[:MAX_BLOBS]
                if (len(kp) == 0):
                    print("no points found")
                break
                if len(kp) >= MIN_BLOBS and len(kp) <= MAX_BLOBS:
                    break
                elif threshold > MIN_THRESHOLD and len(kp) < MIN_BLOBS:
                    threshold /= 1.1
                    print('[INFO] threshold set to %d' % threshold)
                    detector.setHessianThreshold(threshold)
                elif len(kp) > MAX_BLOBS and threshold < MAX_THRESHOLD:
                    threshold *= 1.1
                    print('[INFO] threshold set to %d' % threshold)
                    detector.setHessianThreshold(threshold)
                else:
                    break
            if opts['save'] == True:
                save_keypoints(kp, frame, n_frame, opts)
            if opts['rec'] == True:
                cv2.rectangle(frame, (startX, 0), (endX, h),
			(0, 255, 0), 10)
            if (len(kp) > 0):
                pred = evaluate_classifier(classifier, kp,  frame)
                markers, ghosts = separate(pred, kp)
                frame = cv2.drawKeypoints(frame,markers,None,(0, 255 ,0),4)
                frame = cv2.drawKeypoints(frame,ghosts,None,(0, 0 ,255),4)
            else:
                frame = cv2.drawKeypoints(frame,kp,None,(0, 255 ,0),4)
    if n_frame % (60 / opts['freq']) == 0:
        cv2.imshow("output", cv2.resize(frame, (640, 360)))
    n_frame +=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
