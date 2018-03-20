from run_model import Trained_NN
import sys
functions_path = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection'
sys.path.insert(0, functions_path)
from functions import marker_sequence
import cv2 as cv
import numpy as np
import os
from os.path import join
import pickle

class Trace_Path():
    def __init__(self):
        self.sequences = []
        self.seq_coords = []
        

    def play_video(self, location=os.getcwd(), video_save="resources/output.avi", width = 960, height = 540, flip = True, verbose=False, display=True, save=False, video_path=os.getcwd()+"/output_video.avi"):
        print(video_path)
        cap = cv.VideoCapture(video_path)
        ret, frame = cap.read()
        clone = frame.copy()
        clone = cv.resize(clone, (width,height))
        if(flip): clone = cv.flip(clone, 0)
        cv.namedWindow("Video")
        if (save):
            out_video = cv.VideoWriter(video_save, -1, 20.0, (width,height))
        
        frame_num = 0
        while ret:
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
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
        for i in range(len(self.seq_coords)):
            start = i - path_length
            if start < 0: start = 0
            x_coords = self.seq_coords[i][0][start:i]
            y_coords = self.seq_coords[i][1][start:i]
            for i in range(1,len(x_coords)):
                cv.line(clone, (x_coord[i-1],y_coord[i-1]), (x_coord[i],y_coord[i]), (255,255,0),3)
        return clone


    def unpickle_sequences(self, name="pickle_files/sequences"):
        with open(name + '.pkl','rb') as f:
            self.sequences = pickle.load(f)

        for i in self.sequences:
            self.seq_coords.append(i.coordinates)

    
    
def export_video(video_path=os.join(os.getcwd(),"output_video.avi")):
    path = Trace_Path()
    path.unpickle_sequences()
    path.play_video(video_path=video_path, location=os.getcwd(),save=True, flip=False)

if (__name__=='__main__'):
    export_video()


    



