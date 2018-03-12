from run_model import Trained_NN
import sys
functions_path = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection'
sys.path.insert(0, functions_path)
from functions import analyse
import cv2 as cv
import numpy as np
import os
from os.path import join
import pickle

class Ball():
    def __init__(self, first_point):
        print("New Ball created")
        self.first_point = first_point
        self.pts = []
        self.pts.append(first_point)

class Analyse_Path():
    def __init__(self):
        self.video_coords = []
        self.threshold = 2000
        self.balls = []
    
    def pad(self, arr):
        r = np.zeros((24,24,3))
        r[:arr.shape[0],:arr.shape[1],:arr.shape[2]] = arr
        return r

    def classify(self, nn, location, video='/resources/test_video.mp4', width = 960, height = 540, flip = True, verbose=False, display=True):
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
            global detector
            keypoints, colors, detector, self.threshold, startX, endX = analyse(clone, ssd, classifier, detector, 0, self.threshold, 
                                                                           use_classifier=False)
            if(verbose):
                print("Keypoints: ", len(keypoints))
                print("Colors: ", colors)
                print("detector: ", detector)
                print("threshold: ", self.threshold)
                print("startX: ", startX)
                print("endX: ", endX)
                print("clone shape", clone.shape)
                
            pts = []
            for i in range(len(keypoints)):
                x_img = int(keypoints[i].pt[0])
                y_img = int(keypoints[i].pt[1])
                pt_img = clone[y_img-12:y_img+12, x_img-12:x_img+12]
                pt_img = self.pad(pt_img)
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
                if (len(frame_coords)>0):            
                    self.video_coords.append((frame_num, frame_coords))
                    self.track(10,10)
                    clone = self.draw_paths(clone)
            if (verbose):
                print("-------------------------------------------")
        cap.release()
        cv.destroyAllWindows()

    def get_distance(self, pt1, pt2):
        dist = (pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2
        return dist

    def track_past(self, view_past, current_point, dist, verbose=False):
        past_points = self.video_coords[-view_past:-1]
        for frame in range(len(past_points)-1,-1,-1):
            for point in range(len(past_points[frame][1])):
                if verbose:
                    print("Point: ", past_points[frame][1][point])
                evaluating_point = past_points[frame][1][point]
                evaluating_dist = self.get_distance(current_point, evaluating_point)
                if (evaluating_dist < dist):
                    return evaluating_point
        return
    
    def track(self, start_track, view_past, verbose=False):
        #if verbose:
        print(len(self.video_coords), self.video_coords[-1][0], self.video_coords[-1][1])
        if (len(self.video_coords) > start_track):
            for i in range(len(self.video_coords[-1][1])):
                current_pnt = self.video_coords[-1][1][i]
                last_pnt = self.track_past(view_past, current_pnt, 300)
                pos = self.check_in_balls(last_pnt)
                if not (last_pnt == None):
                    pos = self.check_in_balls(last_pnt)
                    if (pos > -1):
                        if (verbose):
                            print("Current Point: ", current_pnt, " Evaluating: ", last_pnt)
                        self.balls[pos].pts.append(current_pnt)
                    else:
                        print("New ball")
                        self.add_ball(current_pnt)
                else:
                    self.add_ball(current_pnt)
                    print("New ball | Possible false point")
        

    def add_ball(self,first_pnt):
        ball = Ball(first_pnt)
        self.balls.append(ball)

    def check_in_balls(self,last_pnt):
        for i in range(len(self.balls)):
            if self.balls[i].pts[-1] == last_pnt:
                #print("Match")
                return i
        else:
            return -1

    def draw_paths(self, clone):
        for i in range(len(self.balls)):
            clone = self.draw_lines(self.balls[i], clone)
        return clone
    
    def draw_lines(self, ball, clone):
        for i in range(1, len(ball.pts)):
            cv.line(clone, ball.pts[i-1], ball.pts[i], (255,255,0),3)
        return clone

    def save_paths(self):
        return
    
if __name__=='__main__':
    location = "C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection/"
    ssd = cv.dnn.readNetFromCaffe(join(location, 'resources', 'MobileNetSSD_deploy.prototxt'), 
                              join(location, 'resources', 'MobileNetSSD_deploy.caffemodel'))
    classifier = cv.dnn.readNetFromTensorflow(join(location, 'frozen_model.pb'))
    detector = cv.xfeatures2d.SURF_create(2000)
    detector.setUpright(True)
    
    nn = Trained_NN()
    
    analyse_path = Analyse_Path()
    analyse_path.classify(nn,location)
