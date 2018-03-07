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
    required=True,
	help="path to input video")
    ap.add_argument("-p", "--prototxt", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.prototxt'),
	help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.caffemodel'),
	help="path to Caffe pre-trained model"),
    ap.add_argument("--classifier", type=str,
    default=join(root, 'resources', 'frozen_model_reshape_test.pb'))
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
    ap.add_argument("-r", "--rec", type=bool, default=False,
	help="option to draw rectangle")
    ap.add_argument("-s", "--save", type=bool, default=False,
	help="option to save detected keypoints")
    ap.add_argument("--classify", type=bool, default=True,
	help="option to classify marker candidates")
    ap.add_argument("-d", "--dir", type=str, default=join(root, 'saved_images'),
	help="directory to save detected keypoints")
    ap.add_argument("-n", "--noise", type=bool, default=True,
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
classifier = cv2.dnn.readNetFromTensorflow(opts.classifier) # blob classifier

threshold = 2000
detector = cv2.xfeatures2d.SURF_create(threshold) # SURF feature detector
detector.setUpright(True) # we dont need blob orientation

if opts.save:
    try:
        os.mkdir(opts.dir)
    except:
        pass

startX, endX, n_frame = 0, 0, 0
#image_dir = join(root, 'resources', 'Sample_2b')
#image_set0 = list()
#image_set1 = list()
#for i in range(len(os.listdir(image_dir))):
#    for img in os.listdir(image_dir):
#        frame_count = int(img.split('_')[-1].split('.')[0])
#        if frame_count is len(image_set0) and 'video_0' in img:
#            image_set0.append(img)
#        elif frame_count is len(image_set1) and 'video_1' in img:
#            image_set1.append(img)

#total_frame_count = len(image_set0)
#print(total_frame_count)
#hip_seq_0 = func.marker_sequence('white', total_frame_count, 0)
#knee_seq_0 = func.marker_sequence('yellow', total_frame_count, 1)
#ankle_seq_0 = func.marker_sequence('white', total_frame_count, 2)
#hip_seq_1 = func.marker_sequence('white', total_frame_count, 0)
#knee_seq_1 = func.marker_sequence('yellow', total_frame_count, 1)
#ankle_seq_1 = func.marker_sequence('white', total_frame_count, 2)

#vid0_sequences = [hip_seq_0, knee_seq_0, ankle_seq_0]
#vid1_sequences = [hip_seq_1, knee_seq_1, ankle_seq_1]
angle = func.compute_rotation_angle(opts, ssd)

while(True):
    ret, frame = cap.read()
    # video 0
    #try:
    #    frame = cv2.imread(join(image_dir, image_set0[n_frame]))
    #except:
    #    break

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
                                                         use_ssd=opts.noise,
                                                         use_classifier=opts.classify)
    frame = func.plot_with_colors(frame, markers, colors)
    #frame = cv2.drawKeypoints(frame,markers,None,(0, 255 ,0),4)
    #if len(markers) > 3: markers = markers[:3]
    #vid0_sequences = func.set_sequence_coords(vid0_sequences,
    #                                          n_frame, markers)

    cv2.imshow("output", frame)

    n_frame += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

startX, endX, n_frame = 0, 0, 0
#while(True):
    #ret, frame = cap.read()

    # video 2
    #try:
    #    frame = cv2.imread(join(image_dir, image_set1[n_frame]))
    #except:
    #    break
    #frame = cv2.resize(frame, (1920, 1080))
    #markers, colors, detector, threshold, startX, endX = func.analyse(frame, ssd,
#                                                         classifier,
#                                                         detector,
#                                                         n_frame,
#                                                         threshold,
#                                                         startX, endX,
#                                                         verbose=True,
#                                                         crop=False)
#    frame = func.plot_with_colors(frame, markers[:3], colors[:3])
#    if len(markers) > 3: markers = markers[:3]
    #frame = cv2.drawKeypoints(frame,markers,None,(0, 255 ,0),4)
#    vid1_sequences = func.set_sequence_coords(vid1_sequences,
#                                              n_frame, markers)

#    cv2.imshow("output", frame)

#    n_frame += 1
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break


#for seq in vid0_sequences:
#    seq._interpolate()

#for seq in vid1_sequences:
#    seq._interpolate()

#all_sequences = [vid0_sequences, vid1_sequences]

#full_string = func.generate_full_json_string(all_sequences, 2)

#with open('test.json', 'w') as f:
#    json.dump(full_string, f, indent=1)
