from run_model import trained_nn
import sys
functions_path = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection'
sys.path.insert(0, functions_path)
from functions import analyse
import cv2 as cv
import numpy as np
import os
from os.path import join


def pad(arr):
    r = np.zeros((24,24,3))
    r[:arr.shape[0],:arr.shape[1],:arr.shape[2]] = arr
    return r

def classify(nn, location,video='/resources/test_video.mp4', width = 960, height = 540, flip = True, verbose=False, display=True):
    file = location + video
    cap = cv.VideoCapture(file)
    ret, frame = cap.read()
    clone = frame.copy()
    clone = cv.resize(clone, (width,height))
    if(flip): clone = cv.flip(clone, 0)
    cv.namedWindow("Video")
    global move_frame
    threshold = 2000
    video_coords = []
    
    while ret:
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        cv.imshow("Video", clone)
        ret, clone = cap.read()
        clone = cv.resize(clone, (width,height))
        if(flip): clone = cv.flip(clone, 0)
        global detector
        keypoints, colors, detector, threshold, startX, endX = analyse(clone, ssd, classifier, detector, 0, threshold, 
                                                                       use_classifier=False)
        if(verbose):
            print("Keypoints: ", len(keypoints))
            print("Colors: ", colors)
            print("detector: ", detector)
            print("threshold: ", threshold)
            print("startX: ", startX)
            print("endX: ", endX)
            print("clone shape", clone.shape)
            
        pts = []
        for i in range(len(keypoints)):
            x_img = int(keypoints[i].pt[0])
            y_img = int(keypoints[i].pt[1])
            pt_img = clone[y_img-12:y_img+12, x_img-12:x_img+12]
            pt_img = pad(pt_img)
            pts.append(pt_img)
            if (verbose):
                print(x_img, y_img)
                print(pt_img.shape)
                cv.circle(clone, (x_img, y_img), 10, (255,255,255),3)

        if (len(pts) > 0):
            shape = list(pts[0].shape)
            shape[:0] = [len(pts)]
            pts_np = np.concatenate(pts).reshape(shape)
            output = nn.nn_predict(pts_np)
            if (verbose):    
                print("Output predictions: ", output)
            frame_coords = []
            for i in range(len(output)):
                if (output[i] == 0):
                    if (verbose):
                        print("Position of detected: ", i)
                    x_pred = int(keypoints[i].pt[0])
                    y_pred = int(keypoints[i].pt[1])
                    frame_coords.append((x_pred,y_pred))
                    if (display):
                        cv.circle(clone, (x_pred, y_pred), 15, (0,255,0),4)
            video_coords.append(frame_coords)
            
            
        if (verbose):
            print("-------------------------------------------")
        if not ret:
            break
    
    cap.release()
    cv.destroyAllWindows()
    


if __name__=='__main__':
    location = "C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection/"
    ssd = cv.dnn.readNetFromCaffe(join(location, 'resources', 'MobileNetSSD_deploy.prototxt'), 
                              join(location, 'resources', 'MobileNetSSD_deploy.caffemodel'))
    classifier = cv.dnn.readNetFromTensorflow(join(location, 'frozen_model.pb'))
    detector = cv.xfeatures2d.SURF_create(2000)
    detector.setUpright(True)
    
    nn = trained_nn()
    classify(nn,location)
