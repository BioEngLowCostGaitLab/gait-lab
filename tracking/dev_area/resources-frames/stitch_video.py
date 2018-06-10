from run_model import Trained_NN
import os
import sys
functions_path = os.path.join(os.getcwd(),"..","detection")
sys.path.insert(0, functions_path)
from functions import marker_sequence
import cv2 as cv
import numpy as np
import pickle


        
def play_video(save_path, save_format, load_path, width=960, height=540, flip=True, verbose=False):
    print(save_path)
    print(save_format)
    print(load_path)
    
    cap = cv.VideoCapture(video_path)
    ret, frame = cap.read()

    clone = frame.copy()
    clone = cv.resize(frame, (width,height))

    if(flip):
        clone = cv.flip(clone, 0)
    if (display):
        cv.namedWindow("Video")
    
    out_video = cv.VideoWriter(save_path, -1, 20.0, (width,height))
        
    frame_num = 0
    while ret:
            
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
            
        clone = self.draw_paths(clone, frame_num)
            
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

    
def export_video(video_path, video_name, save_path, flip=False):
    path = Trace_Path()
    path.unpickle_sequences(video_name)
    path.play_video(video_path, video_name, save_path, flip=flip, save=True)



if __name__=='__main__':
    



