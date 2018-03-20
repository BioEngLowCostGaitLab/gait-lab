## Needs to be changed to work with sequences

"""
import cv2 as cv
import numpy as np
import os
from os.path import join
import pickle
from analyse_video import Ball

class Trace_Path():
    def __init__(self):
        self.balls = []

    def play_video(self, location, video='/resources/test_video.mp4', width = 960, height = 540, flip = True, verbose=False, display=True, save=False, video_path=os.getcwd()+"/output_video.avi"):
        file = location + video
        cap = cv.VideoCapture(file)
        ret, frame = cap.read()
        clone = frame.copy()
        clone = cv.resize(clone, (width,height))
        if(flip): clone = cv.flip(clone, 0)
        cv.namedWindow("Video")
        if (save):
            out_video = cv.VideoWriter('output.avi', -1, 20.0, (width,height))
        
        frame_num = 0
        while ret:
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            ## Drawing performed here

            clone = self.draw_paths(clone, frame_num)
        
            if (save):
                out_video.write(clone)
            cv.imshow("Video", clone)
            frame_num += 1
            ret, clone = cap.read()
            if not ret:
                break
            clone = cv.resize(clone, (width,height))
            if(flip): clone = cv.flip(clone, 0)
            
        cap.release()
        if (save):
            out_video.release()
        cv.destroyAllWindows()

    def draw_paths(self, clone, frame_num, path_length=10):
        #for i in range(len(self.balls)):
        clone = self.draw_lines(self.balls[0], clone, frame_num, path_length)
        return clone
    
    def draw_lines(self, ball, clone, frame_num, path_length):
        position = self.draw_from_position(frame_num, ball)
        if not position == None:
            
            end = self.iterate_end(position+ball.iter_pos, path_length)
            print("Position: ", position, " | Position, Ball Pos: ", position+ball.iter_pos, " | End: ", end)
            for i in range(position, end, -1):
                #print(i)
                cv.line(clone, ball.pts[i-1][1], ball.pts[i][1], (255,255,0),3)
            
        return clone

    def unpickle_balls(self, name="balls"):
        with open(name + '.pkl','rb') as f:
            self.balls = pickle.load(f)

    def iterate_end(self, position, path_length = 10):
        if position - path_length < 0:
            end = -1
        else:
            end = position - path_length
        return end
##        pos = []
##        for i in range(position, end, -1):
##            pos.append(i)
##        return pos

    def draw_from_position(self, frame_num, ball):
        print("Frame: ", frame_num, " | Iter: ", ball.iter," | Iter Pos: ", ball.iter_pos)
        if frame_num < ball.iter:
            return
        elif frame_num == ball.iter:
            return 0
        elif frame_num > ball.iter:
            ##check if greater than max then change value
            ball.iter_pos += 1
            ball.iter = ball.pts[ball.iter_pos][0]
            return 1

def export_video(video_path=os.getcwd()+"/output_video.avi"):
    path = Trace_Path()
    path.unpickle_balls()
    path.play_video(location,save=True, video_path=video_path)
    
if (__name__=='__main__'):
    location = "C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection/"
    #path = Trace_Path()
    #path.unpickle_balls()
    #path.play_video(location)
    export_video()


"""
