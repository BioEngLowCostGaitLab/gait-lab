from run_model import Trained_NN
import os
import sys
functions_path = os.path.join(os.getcwd(),"..","detection")
sys.path.insert(0, functions_path)
from functions import marker_sequence
import cv2 as cv
import numpy as np
import pickle

class Trace_Path():
    def __init__(self, video_path,video_name):
        self.sequences = []
        self.seq_coords = []
        self.video_path = video_path
        self.video_name = video_name
        
    def play_video(self, save_path, width = 960, height = 540, flip = True, verbose=False, display=True, save=False):
        cap = cv.VideoCapture(self.video_path)
        ret, frame = cap.read()
        clone = frame.copy()
        clone = cv.resize(clone, (width,height))
        
        if(flip):
            clone = cv.flip(clone, 0)
        if (display):
            cv.namedWindow("Video")
        if (save):
            out_video = cv.VideoWriter(save_path, -1, 20.0, (width,height))
        
        frame_num = 0
        while ret:
            print(frame_num)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
            ##clone = self.draw_paths(clone, frame_num)
            
            if (display):
                cv.imshow("Video", clone)
            if (save):
                out_video.write(clone)
            
            frame_num += 1
            ret, clone = cap.read()
            if not ret:
                break
            clone = cv.resize(clone, (width,height))
            if(flip):
                clone = cv.flip(clone, 0)
            
        cap.release()
        if (save):
            out_video.release()
        cv.destroyAllWindows()

    def draw_paths(self, clone, frame_num, path_length=10):
        for i in range(len(self.seq_coords)):
            start = i - path_length
            if start < 0: start = 0
            x_coords = self.seq_coords[i][0][start:i]
            y_coords = self.seq_coords[i][1][start:i]
            for i in range(1,len(x_coords)):
                cv.line(clone, (x_coord[i-1],y_coord[i-1]), (x_coord[i],y_coord[i]), (255,255,0),3)
        return clone


    def unpickle_sequences(self, video_name):
        with open("pickle_files/sequences_" + video_name + '.pkl','rb') as f:
            self.sequences = pickle.load(f)
            
        for i in self.sequences:
            self.seq_coords.append(i.coordinates)

    
def export_video(video_path, video_name, save_path, flip=False):
    path = Trace_Path(video_path,video_name)
    path.unpickle_sequences(video_name)
    path.play_video(save_path,flip, save=True)



    



