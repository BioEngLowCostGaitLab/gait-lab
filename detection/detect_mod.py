import cv2
import functions_mod as func
import numpy as np
import argparse
import sys
import os
from os.path import join
import json

root = os.getcwd()

def get_args(root):
    # user defined arguments, video file in onedrive, ask Antti
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
    required=True,
	help="path to input video")
    ap.add_argument("-p", "--prototxt", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.prototxt'),
	help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.caffemodel'),
	help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--classifier", type=str,
    default=join(root, 'resources', 'frozen_model_reshape_test.pb'),
	help="path to Caffe pre-trained model")
    ap.add_argument("-r", "--rec", type=bool, default=False,
	help="option to draw rectangle")
    ap.add_argument("-o", "--out", type=str, required=True,
	help="output file name")
    ap.add_argument("-n", "--noise", type=bool, default=False,
	help="option to detect person and narrow down search area")


    return ap.parse_args()

opts = get_args(root)

cap = cv2.VideoCapture(opts.video)

ssd = cv2.dnn.readNetFromCaffe(opts.prototxt, opts.model) # SSD person detector
classifier = cv2.dnn.readNetFromTensorflow(opts.classifier) # blob classifier

threshold = 2000
detector = cv2.xfeatures2d.SURF_create(threshold) # SURF feature detector
detector.setUpright(True) # we dont need blob orientation


startX, endX, n_frame = 0, 0, 0

f = open(opts.out, 'w')

angle = compute_optimal_rotation(opts.video, ssd)
print('angle is %i' % (angle))



while(True):
    ret, frame = cap.read()

    frame = np.rot90(frame, angle)

    frame = cv2.resize(frame, (1920, 1080))
    markers, colors, detector, threshold, startX, endX = func.analyse(frame, ssd,
                                                         classifier,
                                                         detector,
                                                         n_frame,
                                                         threshold,
                                                         startX, endX,
                                                         verbose=True,
                                                         crop=False,
                                                         use_ssd=opts.noise)
    frame = func.plot_with_colors(frame, markers, colors)

    for m in markers:
        f.write('%d, %.3f, %.3f\n' % (n_frame, m.pt[0], m.pt[1]))
        # frame number, x-coord, y-coord csv


    cv2.imshow("output", frame)

    n_frame += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
