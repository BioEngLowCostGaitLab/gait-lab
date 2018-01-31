import cv2 as cv
import numpy as np
from functions import analyse
import os
from os.path import join
from datetime import datetime as dt

def frame_stamp():
    current = dt.now()
    out_str = (str(current.year) + str(current.month) + str(current.day) + "_" + 
               str(current.hour) + str(current.minute) + str(current.second) + "_" +
               str(current.microsecond) + "_" + "frame")
    return out_str

##Global Variables

move_frame = False
isBall = 0
pts = []

def next_frame(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        global pts
        pts = []
        pts.append(x)
        pts.append(y)
        global move_frame
        move_frame = True
        global isBall
        isBall = 1
    if event == cv.EVENT_RBUTTONDOWN:
        pts = []
        pts.append(x)
        pts.append(y)
        move_frame = True
        isBall = 0
        
def classify(file = 'resources/test_video.mp4', width = 960, height = 540, flip = True):
    cap = cv.VideoCapture(file)
    ret, frame = cap.read()
    clone = cv.resize(frame, (width,height))
    if(flip): clone = cv.flip(clone, 0)
    cv.namedWindow("Video")
    cv.setMouseCallback("Video", next_frame)
    global move_frame
    global isBall

    ## Loop to classify Images
    while ret:
        cv.imshow("Video", clone)
        key = cv.waitKey(1)
        
        skip = False
        if (key == 113):
            break
        if (key == 46):
            skip = True
        
        ## When image is classified or frame is skipped
        if (move_frame or skip):
            ret, frame = cap.read()
            clone = cv.resize(frame, (width,height))
            if(flip): clone = cv.flip(clone, 0)
            if (move_frame):
                move_frame = False
                roi = clone[pts[1]-12:pts[1]+12, pts[0]-12:pts[0]+12]
                #cv.imshow("ROI", roi)
                cv.imwrite("./labels/" + str(isBall) + "_" + frame_stamp() + ".jpg", roi)
                #cv.waitKey(0)
                #cv.destroyWindow("ROI")
                isBall = 0
    cap.release()
    cv.destroyAllWindows()
    
    
def play_video(file = 'resources/test_video.mp4', width = 960, height = 540, flip = True):
    cap = cv.VideoCapture(file)
    ret, frame = cap.read()
    clone = cv.resize(frame, (width,height))
    if(flip): clone = cv.flip(clone, 0)
    while ret:
        cv.imshow("Input", clone)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
        clone = cv.resize(frame, (width,height))
        if(flip): clone = cv.flip(clone, 0)
    cap.release()
    cv.destroyAllWindows()


classify()



