import cv2 as cv
import numpy as np
import os
from os.path import join
#from analyse_video import Ball

class Trace_Path():
    def __init__(self):
        self.balls = []

    def play_video(self, location, video='/resources/test_video.mp4', width = 960, height = 540, flip = True, verbose=False, display=True):
        file = location + video
        cap = cv.VideoCapture(file)
        ret, frame = cap.read()
        clone = frame.copy()
        clone = cv.resize(clone, (width,height))
        if(flip): clone = cv.flip(clone, 0)
        cv.namedWindow("Video")
        frame_num = 0
        while ret:
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            cv.imshow("Video", clone)
            frame_num += 1
            ret, clone = cap.read()
            if not ret:
                break
            clone = cv.resize(clone, (width,height))
            if(flip): clone = cv.flip(clone, 0)
        cap.release()
        cv.destroyAllWindows()

    def draw_paths(self, clone):
        for i in range(len(self.balls)):
            clone = self.draw_lines(self.balls[i], clone)
        return clone
    
    def draw_lines(self, ball, clone):
        for i in range(1, len(ball.pts)):
            cv.line(clone, ball.pts[i-1], ball.pts[i], (255,255,0),3)
        return clone

if (__name__=='__main__'):
    location = "C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection/"
    path = Trace_Path()
    path.play_video(location)
    
