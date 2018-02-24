import sys
functions_path = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection'
sys.path.insert(0, functions_path)
from functions import analyse
import cv2 as cv
import numpy as np
import os
from os.path import join
from datetime import datetime as dt

# Features include: frame number, coordinate (x,y), image (extracted from coord and frame number)
# Global variables
image_pos = 0
seq_pos = 0
move_frame = False
isBall = 0
pts = []

def frame_stamp():
    current = dt.now()
    out_str = (str(current.year) + str(current.month) + str(current.day) + "_" +
               str(current.hour) + str(current.minute) + str(current.second) + "_" +
               str(current.microsecond) + "_" + "frame")
    return out_str

def last_image_name():
    fdir = "seq_labels"
    dataset = []
    lf = ""
    for file in os.listdir(fdir):
        if file.endswith(".jpg"):
            lf = file
    return lf

def set_seq_pos():
    global seq_pos
    temp = last_image_name()
    if temp != "":
        temp = temp[2]
        seq_pos = int(temp) + 1

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
        
def classify(file = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection/resources/test_video.mp4', width = 960, height = 540, flip = True):
    set_seq_pos()
    cap = cv.VideoCapture(file)
    ret, frame = cap.read()
    clone = cv.resize(frame, (width,height))
    if(flip): clone = cv.flip(clone, 0)
    cv.namedWindow("Video")
    cv.setMouseCallback("Video", next_frame)
    global move_frame
    global isBall
    global image_pos
    
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
            if (move_frame):
                move_frame = False
                roi = clone[pts[1]-12:pts[1]+12, pts[0]-12:pts[0]+12]
                ## Saves image to seq_labels file, to be used as training data
                cv.imwrite("./seq_labels/" + str(isBall) + "_" + str(seq_pos) + "_" + str(image_pos) + "_" 
                           + str(pts[0]) + "_" + str(pts[1]) + "_" + frame_stamp() + ".jpg", roi)
                isBall = 0
            image_pos += 1
            ret, frame = cap.read()
            clone = cv.resize(frame, (width,height))
            if(flip): clone = cv.flip(clone, 0)
    cap.release()
    cv.destroyAllWindows()
    
    
def play_video(file = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection/resources/test_video.mp4', width = 960, height = 540, flip = True):
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



if __name__ == '__main__':
    print("Running classifier...")
    classify()
