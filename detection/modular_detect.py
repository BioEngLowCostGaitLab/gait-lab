import cv2
import functions as func
import numpy as np
import argparse
import sys
import os
from os.path import join
import json

def get_args(root):
    # user defined arguments, video file in onedrive, ask Antti
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
    default='',
	help="path to input video"),
    ap.add_argument("-p", "--prototxt", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.prototxt'),
	help="path to Caffe 'deploy' prototxt file"),
    ap.add_argument("-m", "--model", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.caffemodel'),
	help="path to Caffe pre-trained model"),
    ap.add_argument("--classifier", type=str,
    default=join(root, 'resources', 'frozen_model_reshape_test.pb'))
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections"),
    ap.add_argument("-r", "--rec", type=bool, default=True,
	help="option to draw rectangle"),
    ap.add_argument("-s", "--save", type=bool, default=False,
	help="option to save detected keypoints"),
    ap.add_argument("--classify", type=bool, default=True,
	help="option to classify marker candidates"),
    ap.add_argument("--savedir", type=str, default=join(root, 'demo_saved_images'),
	help="directory to save detected keypoints"),
    ap.add_argument("-n", "--noise", type=bool, default=True,
	help="option to detect person and narrow down search area"),
    ap.add_argument("--phone", type=bool, default=False,
    help="option to use phone recorded video versus webcam captured images"),
    ap.add_argument("--imgdir0", type=str, default='',
    help="directory that contains webcam captured images"),
    ap.add_argument("--imgdir1", type=str, default='',
    help="directory that contains webcam captured images"),
    ap.add_argument("--videonumber", type=int, default=0,
    help="which video from the whole set")


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
print(root)
opts = get_args(root)


ssd = cv2.dnn.readNetFromCaffe(opts.prototxt, opts.model) # SSD person detector, files from https://github.com/chuanqi305/MobileNet-SSD
classifier = cv2.dnn.readNetFromTensorflow(opts.classifier) # blob classifier

threshold = 1e4
detector = cv2.xfeatures2d.SURF_create(threshold) # SURF feature detector
detector.setUpright(True) # we dont need blob orientation
if opts.save:
    try:
        os.mkdir(opts.savedir)
    except:
        pass

startX, endX, n_frame = 0, 0, 0

if not opts.phone:

    image_set0 = list()
    for i in range(len(os.listdir(opts.imgdir0))):
        for img in os.listdir(opts.imgdir0):
            frame_count = int(img.split('_')[-1].split('.')[0])
            if frame_count is len(image_set0) and 'video' in img:
                image_set0.append(img)
    image_set1 = list()
    for i in range(len(os.listdir(opts.imgdir1))):
        for img in os.listdir(opts.imgdir1):
            frame_count = int(img.split('_')[-1].split('.')[0])
            if frame_count is len(image_set1) and 'video' in img:
                image_set1.append(img)
    image_sets = [image_set0, image_set1]
    total_frame_count = len(image_set0)

else:
    cap = cv2.VideoCapture(opts.video)
    angle = func.compute_rotation_angle(opts.video, ssd)

seq00 = func.marker_sequence(0, total_frame_count, 0)
seq01= func.marker_sequence(0, total_frame_count, 1)
seq02 = func.marker_sequence(0, total_frame_count, 2)
sequences0 = [seq00, seq01, seq02]

seq10 = func.marker_sequence(0, total_frame_count, 0)
seq11= func.marker_sequence(0, total_frame_count, 1)
seq12 = func.marker_sequence(0, total_frame_count, 2)
sequences1 = [seq10, seq11, seq12]

sequences = [sequences0, sequences1]

dirs = [opts.imgdir0, opts.imgdir1]

for i, video in enumerate(image_sets):
    startX, endX, n_frame = 0, 0, 0
    while(True):
        if opts.phone:
            ret, frame = cap.read()
            frame = np.rot90(frame, angle)
        else:
            try:
                frame = cv2.imread(join(dirs[i], video[n_frame]))
            except:
                break

            frame = cv2.resize(frame, (1920, 1080))
            markers, colors, detector, threshold, startX, endX = func.analyse(frame, ssd,
                                                            classifier,
                                                            detector,
                                                            n_frame,
                                                            threshold,
                                                            startX, endX,
                                                            verbose=True,
                                                            crop=False,
                                                            use_ssd=True,
                                                            use_classifier=True)
            if opts.save: func.save_keypoints(markers, frame, n_frame, opts)
            if len(markers) > 3: markers = markers[:3]
            frame = func.plot_with_colors(frame, markers, colors)
    #frame = cv2.drawKeypoints(frame,markers,None,(0, 255 ,0),4)
            sequences[i] = func.set_sequence_coords(sequences[i], n_frame, markers)
    #if opts.rec and opts.noise: cv2.rectangle(frame, (startX, int(0.35 * 1080)), (endX, 1080),
    #(0, 255, 0), 10)
        cv2.imshow("output", cv2.resize(frame, (640, 360)))

        n_frame += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


        for seq in sequences[i]:
            seq._interpolate()
            seq._remove_nan()




full_string = func.generate_full_json_string(sequences, 2, total_frame_count)
with open('demo.json', 'w') as f:
    json.dump(full_string, f, indent=1)
