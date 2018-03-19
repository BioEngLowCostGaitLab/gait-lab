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
    ball_id = 0
    def __init__(self, first_point, first_frame):
        self.id = Ball.ball_id
        Ball.ball_id += 1
        
        print("#q")
        print("ID: ", self.id)
        print("Ball_ID: ", Ball.ball_id)
        print("New Ball created: ", first_point, first_frame)
        print("################################")
        
        self.pts = []
        self.pts.append((first_frame, first_point))
        
        self.iter = first_frame
        self.iter_pos = 0

    def add_point(self, frame, point):
        self.pts.append((frame, point))

class Analyse_Path():
    def __init__(self, threshold = 2000, start_analysis = 5):
        self.video_coords = []
        self.threshold = threshold
        self.balls = []
        self.start_analysis = start_analysis
        self.frames_objects = []
    
    def pad(self, arr):
        r = np.zeros((24,24,3))
        r[:arr.shape[0],:arr.shape[1],:arr.shape[2]] = arr
        return r

    def classify(self, nn, location, video='/tracking/resources/20180205_135429.mp4', width = 960, height = 540, flip = True, verbose=False, display=True,path=True):
        file = location + video
        cap = cv.VideoCapture(file)
        ret, frame = cap.read()
        clone = frame.copy()
        clone = cv.resize(clone, (width,height))
        if(flip): clone = cv.flip(clone, 0)
        cv.namedWindow("Video")

        frame_num = 0
        while ret:
            self.current_frame_objects = []
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            cv.imshow("Video", clone)
            frame_num += 1
            ret, clone = cap.read()
            if not ret:
                break
            clone = cv.resize(clone, (width*2,height*2))
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
                    cv.circle(clone, (x_img, y_img), 10, (255,255,255), 3)

            if (path & len(pts) > 0):
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
                    self.track(self.start_analysis,10)
                    clone = self.draw_paths(clone)
            clone = cv.resize(clone, (width,height))
            print("Current frame objects: ", self.current_frame_objects)
            print("-------------------------------------------")
            if (verbose):
                print("-------------------------------------------")
        cap.release()
        cv.destroyAllWindows()

    def get_distance(self, pt1, pt2):
        dist = (pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2
        return (dist)**0.5

    def track_past(self, position, view_past, current_point, dist, verbose=False):
        past_points = self.video_coords[-view_past:-1]
        for frame in range(len(past_points)-1,-1,-1):
            for point in range(len(past_points[frame][1])):
                if verbose:
                    print("Point: ", past_points[frame][1][point])
                evaluating_point = past_points[frame][1][point]
                evaluating_dist = self.get_distance(current_point, evaluating_point)
                if (evaluating_dist < dist * (position+1)):
                    return evaluating_point
        return
    
    def track(self, start_track, view_past, verbose=False):
        #if verbose:
        print(len(self.video_coords), self.video_coords[-1][0], self.video_coords[-1][1])
        if (len(self.video_coords) > start_track):
            for i in range(len(self.video_coords[-1][1])):
                print("POsition: ", i)
                current_pnt = self.video_coords[-1][1][i]
                last_pnt = self.track_past(i, view_past, current_pnt, 30)
                pos = self.check_in_balls(last_pnt)
                if not (last_pnt == None):
                    pos = self.check_in_balls(last_pnt)
                    if (pos > -1):
                        if (verbose):
                            print("Position: ", pos, " Current Point: ", current_pnt, " Evaluating: ", last_pnt, "Frame: ", self.video_coords[-1][0]," Ball: ", self.balls[pos])
                        self.balls[pos].add_point(self.video_coords[-1][0], current_pnt)
                    else:
                        print("New ball")
                        current_id = self.add_ball(self.video_coords[-1][0],current_pnt)
                        self.current_frame_objects.append(current_id)
                else:
                    print("New ball | Possible false point")
                    current_id = self.add_ball(self.video_coords[-1][0],current_pnt)
                    self.current_frame_objects.append(current_id)
        

    def add_ball(self, first_frame, first_pnt):
        ball = Ball(first_pnt, first_frame)
        self.balls.append(ball)
        return ball.id

    def check_in_balls(self,last_pnt):
        for i in range(len(self.balls)):
            if self.balls[i].pts[-1][1] == last_pnt:
                return i
        else:
            return -1

    def draw_paths(self, clone):
        for i in range(len(self.balls)):
            clone = self.draw_lines(self.balls[i], clone)
        return clone
    
    def draw_lines(self, ball, clone):
        for i in range(1, len(ball.pts)):
            cv.line(clone, ball.pts[i-1][1], ball.pts[i][1], (255,255,0),3)
        return clone

    def save_paths(self):
        return

    def pickle_balls(self, name="balls"):
        with open(name + '.pkl','wb') as f:
            pickle.dump(self.balls,f)
    
if __name__=='__main__':
    location = "C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/"
    ssd = cv.dnn.readNetFromCaffe(join(location, 'detection/resources', 'MobileNetSSD_deploy.prototxt'), 
                              join(location, 'detection/resources', 'MobileNetSSD_deploy.caffemodel'))
    classifier = cv.dnn.readNetFromTensorflow(join(location, 'detection/frozen_model.pb'))
    detector = cv.xfeatures2d.SURF_create(2000)
    detector.setUpright(True)
    
    nn = Trained_NN()
    
    analyse_path = Analyse_Path()
    vid_path1 = 'detection/resources/test_video.mp4'
    vid_path2 = 'detection/resources/20180205_135429.mp4'
    vid_path3 = 'detection/resources/20180205_135556.mp4'
    analyse_path.classify(nn,location,video=vid_path2,flip=False, verbose=True)
    analyse_path.pickle_balls()
