import cv2
from functions import analyse, plot_with_colors
import numpy as np
import argparse
import sys
import os
from os.path import join

def get_args(root):
    # user defined arguments, video file in onedrive, ask Antti
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
    default = join(root, 'resources', '20180205_135556.mp4'),
	help="path to input video")
    ap.add_argument("-p", "--prototxt", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.prototxt'),
	help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.caffemodel'),
	help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
    ap.add_argument("-r", "--rec", type=bool, default=False,
	help="option to draw rectangle")
    ap.add_argument("-f", "--freq", type=int, default=60,
	help="number of images to show per 1 second of footage")
    ap.add_argument("-s", "--save", type=bool, default=False,
	help="option to save detected keypoints")
    ap.add_argument("-cl", "--classify", type=bool, default=False,
	help="option to classify marker candidates")
    ap.add_argument("-d", "--dir", type=str, default=join(root, 'saved_images'),
	help="directory to save detected keypoints")
    ap.add_argument("-n", "--noise", type=bool, default=False,
	help="option to detect person and narrow down search area")


    return ap.parse_args()

root = os.getcwd()
try:
    dirs = sys.argv[0].split('\\')[1:-1]
    if len(dirs) > 0:
        root = 'C:\\'
        for i in range(len(dirs)):
            root = join(root, dirs[i])
except:
    pass

opts = get_args(root)

cap = cv2.VideoCapture(opts.video)

ssd = cv2.dnn.readNetFromCaffe(opts.prototxt, opts.model) # SSD person detector
classifier = cv2.dnn.readNetFromTensorflow(join(root, 'frozen_model_reshape_test.pb')) # blob classifier

threshold = 2000
detector = cv2.xfeatures2d.SURF_create(threshold) # SURF feature detector
detector.setUpright(True) # we dont need blob orientation

if opts.save:
    try:
        os.mkdir(opts.dir)
    except:
        pass

startX, endX, n_frame = 0, 0, 0

while(True):
    ret, frame = cap.read()
    markers, colors, detector, threshold, startX, endX = analyse(frame, ssd,
                                                         classifier,
                                                         detector,
                                                         n_frame,
                                                         threshold,
                                                         startX, endX)
    frame = plot_with_colors(frame, markers, colors)

    cv2.imshow("output", frame)

    n_frame += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
