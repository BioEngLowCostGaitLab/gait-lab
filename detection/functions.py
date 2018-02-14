from __future__ import print_function
import cv2
import numpy as np
import argparse
from os.path import join
import os
from time import time
import sys
import json
from scipy.interpolate import interp1d


def evaluate_ssd(ssd, frame, startX, endX):
    # args: network, frame, number of passed frames, number of frame in which person was last found, opts
    # returns: top left corner and bottom right corner of rectangle in which person lies,
    # number of frame in which person was last found
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
    (300, 300), 127.5)
    found = False
    ssd.setInput(blob)
    detections = ssd.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            if idx == 15: # person detected
                found = True
                conf_f = confidence
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startXn, startY, endXn, endY) = box.astype("int")
    if found:
        return startXn, endXn, conf_f
    else:
        return startX, endX, 0

def evaluate_classifier(classifier, kp, frame):
    images = get_keypoint_images(kp, frame)
    input = cv2.dnn.blobFromImages(images)
    classifier.setInput(input)
    output = classifier.forward()
    colors = list()
    for i in range(len(output)):
        if output[i] > 0.5:
            colors.append(get_marker_color(images[i]))
    return output, colors

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

def filter_kp(kp, h, w, startX):
    # filtering criteria: must be smaller than maximum diameter
    max_size = w * 0.06  # maximum diameter of keypoint
    filtered = []

    for i in range(len(kp)):
        if kp[i].size < max_size:
            # filtering criteria met
            filtered.append(kp[i])

    for i in range(len(filtered)):
        # move the keypoint to match their location in the image
        filtered[i].pt = (filtered[i].pt[0] + startX, filtered[i].pt[1] + int(0.35 * h))

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
    return markers, ghosts

def get_marker_color(image):
    colors = 1.0 * np.array([[255, 255, 255], [0, 255, 255]])
    pixel = image[12,12]
    errors = np.array([0, 0])
    for i in range(2):
        for j in range(2):
            errors[i] += (pixel[j] - colors[i, j]) ** 2
    index = np.argmin(errors)
    return tuple(colors[index, :])

def plot_with_colors(frame, kp, colors):
    for i in range(len(colors)):
        #if sum(colors[i]) > 0:
        frame = cv2.drawKeypoints(frame, [kp[i]], None, colors[i], 4)
    return frame


def analyse(frame, ssd, classifier, detector, n_frame, threshold, startX=0, endX=0,
            MIN_BLOBS=6, MAX_BLOBS=12, MIN_THRESHOLD=5e2, MAX_THRESHOLD=5e4,
            use_ssd=True, use_classifier=True, start_frame=0, verbose=False, flip=False):
    if not frame.shape[:2] == (1080, 1920):
        frame = cv2.resize(frame, (1920, 1080))
    if flip:
        frame = cv2.flip(frame, 0)
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.uint8)
    (h, w) = frame.shape[:2]
    if n_frame >= start_frame:
        if use_ssd:
            startX, endX, confidence = evaluate_ssd(ssd, frame, startX, endX)
            if verbose: print('[INFO] p: %.2f%%' % (confidence * 100))
            startX, endX = startX - int(0.2 * (endX - startX)), endX + int(0.1 * (endX - startX))
            if (endX > w - 12):
                endX = w - 12
            if (startX < 12):
                startX = 12
        else:
            startX = 12
            endX = w - 12
        grey_frame = grey_frame[int(0.35 * h):, startX:endX]
        while True:
            # adaptive filtering:
            # we want to find between 12-24 blobs in this particular video (4-8 times the actual number of markers visible)
            # the detection threshold of the SURF detector is adjusted according to that withing reasonable range
            # this is faster than setting a low threshold and removing the worst detections
            kp = detector.detect(grey_frame, None)
            kp = filter_kp(kp, h, w, startX)
            if len(kp) >= MIN_BLOBS and len(kp) <= MAX_BLOBS:
                break
            elif threshold > MIN_THRESHOLD and len(kp) < MIN_BLOBS:
                threshold /= 1.05
                if verbose: print('[INFO] threshold set to %d' % threshold)
                detector.setHessianThreshold(threshold)
            elif len(kp) > MAX_BLOBS and threshold < MAX_THRESHOLD:
                threshold *= 1.05
                if verbose: print('[INFO] threshold set to %d' % threshold)
                detector.setHessianThreshold(threshold)
            else:
                break
        markers = kp

        if (len(kp) > 0 and use_classifier):
            pred, colors = evaluate_classifier(classifier, kp,  frame)
            markers, ghosts = separate(pred, kp)

        return markers, colors, detector, threshold, startX, endX



class marker_sequence:
    def __init__(self, colour, total_frame_count, id):

        self.colour = colour
        self.coordinates = np.zeros([2, total_frame_count])
        self.id = id

    def set_coordinates(self, coords, frame):
        self.coordinates[:,frame] = coords

def generate_video_json_dict(sequences,
                                camera):
    total_frame_count = np.shape(sequences[1].coordinates)[1]
    imglist = list()
    for frame in range(total_frame_count):
        ptslist = list()
        for seq in sequences:
            if not all(seq.coordinates[:,frame]) == 0:
                d = {
                    'colour': seq.colour, 'coords': list(seq.coordinates[:,frame]),
                    'id': seq.id
                }
                print(d)
                ptslist.append(d)

        image_dict = {'frame': frame, 'ptslist': ptslist}
        imglist.append(image_dict)

    out = {'camera': camera, 'imglist': imglist}
    return out

def generate_full_json_string(all_sequences, camera_count):

    markerpts = list()

    for camera in range(camera_count):
        markerpts.append(generate_video_json_dict(all_sequences[camera], camera))

    out = {'markerpts': markerpts}
    return out


def interpolate(sequence):
    regions = list()
    frame_count = sequence.shape[1]
    k = 0

    x, y = sequence[0,:], sequence[1, :]

    while x[k] == 0:
        k += 1
    while (k < frame_count):
        while not x[k] == 0
            k += 1
