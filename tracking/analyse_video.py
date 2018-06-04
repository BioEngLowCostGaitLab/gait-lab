from run_model import Trained_NN
import os
import sys
functions_path = os.path.join(os.getcwd(),"..","detection")
sys.path.insert(0, functions_path)
from functions import analyse, marker_sequence
import cv2 as cv
import numpy as np
import pickle



class Ball():
    ball_id = 0
    def __init__(self, first_point, first_frame, verbose=False):
        self.id = Ball.ball_id
        Ball.ball_id += 1        
        self.pts = []
        self.pts.append((first_frame, first_point))
        
        self.iter = first_frame
        self.iter_pos = 0

    def add_point(self, frame, point):
        self.pts.append((frame, point))




class Analyse_Path():
    def __init__(self, threshold = 2000, start_analysis = 5, display = True):
        self.video_coords = []
        self.threshold = threshold
        self.balls = []
        self.start_analysis = start_analysis
        self.frames_objects = []
        self.display = display
    
    def pad(self, arr):
        r = np.zeros((24,24,3))
        r[:arr.shape[0],:arr.shape[1],:arr.shape[2]] = arr
        return r

    def classify(self, nn, video_path, video_name, video_format, ssd, detector, width = 960, height = 540, flip = True, verbose=False, display=True,detect_classifier="",draw_circles=False,draw_kp=False):
        cap = cv.VideoCapture(video_path)
        save_path = os.path.join(video_path,"..","..","analysed_videos",video_name + video_format)
        out_video = cv.VideoWriter(save_path, -1, 20.0, (width,height))
        ret, frame = cap.read()
        clone = frame.copy()
        clone = cv.resize(clone, (width,height))
        
        if(flip): clone = cv.flip(clone, 0)
        if (display):
            cv.namedWindow("Video")
            
        frame_num = 0
        while ret:
            self.current_frame_objects = []
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            if (display):
                cv.imshow("Video", clone)
            frame_num += 1
            out_video.write(clone)
            ret, clone = cap.read()
            if not ret:
                break
            clone = cv.resize(clone, (width*2,height*2))
            if(flip): clone = cv.flip(clone, 0)
            classifier = detect_classifier
            if (detect_classifier==""):
                use_class = False
            else:
                use_class = True
            keypoints, colors, detector, self.threshold, startX, endX = analyse(clone, ssd, detect_classifier, detector, 0, self.threshold,
                                                                                    use_classifier=use_class, crop=False)  
            if(verbose):
                print("Keypoints: ", len(keypoints))
                print("Colors: ", colors)
                print("detector: ", detector)
                print("threshold: ", self.threshold)
                print("startX: ", startX)
                print("endX: ", endX)
                print("clone shape", clone.shape)

            if (use_class == False):
                ## Convert pad keypoints detected and store in pts
                pts = []
                for i in range(len(keypoints)):
                    x_img = int(keypoints[i].pt[0])
                    y_img = int(keypoints[i].pt[1])
                    pt_img = clone[y_img-12:y_img+12, x_img-12:x_img+12]
                    pt_img = self.pad(pt_img)
                    pts.append(pt_img)
                    if (verbose):
                        print(x_img, y_img)
                    if (draw_circles):
                        cv.circle(clone, (x_img, y_img), 10, (255,255,255), 3)
                ## Use different cnn on data
                if (len(pts)>0):
                    shape = list(pts[0].shape)
                    shape[:0] = [len(pts)]
                    pts_np = np.concatenate(pts).reshape(shape)
                    output = nn.nn_predict(pts_np)
                    if (verbose):    
                        print("Output predictions: ", output)

            frame_coords = []
            for i in range(len(keypoints)):
                if (verbose):
                    print("Position of detected: ", i)
                if (use_class or output[i] == 0):
    
                    x_pred = int(keypoints[i].pt[0])
                    y_pred = int(keypoints[i].pt[1])
                    frame_coords.append((x_pred,y_pred))
                        
                if (draw_circles):
                    cv.circle(clone, (x_pred, y_pred), 15, (0,255,0),4)

            if (draw_kp):
                clone = cv.drawKeypoints(clone, keypoints, None, (0,255,0), 4)
            if (len(frame_coords)>0):            
                self.video_coords.append((frame_num, frame_coords))
                self.track(self.start_analysis,10)
            clone = self.draw_paths(clone)
            clone = cv.resize(clone, (width,height))
            self.frames_objects.append(self.current_frame_objects)
            if (verbose):
                print("Current frame objects: ", self.current_frame_objects)
                print("-------------------------------------------")
        out_video.release()
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
        if verbose:
            print(len(self.video_coords), self.video_coords[-1][0], self.video_coords[-1][1])
        if (len(self.video_coords) > start_track):
            for i in range(len(self.video_coords[-1][1])):
                current_pnt = self.video_coords[-1][1][i]
                last_pnt = self.track_past(i, view_past, current_pnt, 55)
                pos = self.check_in_balls(last_pnt)
                if not (last_pnt == None):
                    pos = self.check_in_balls(last_pnt)
                    if (pos > -1):
                        if (verbose):
                            print("Position: ", pos, " Current Point: ", current_pnt, " Evaluating: ", last_pnt, "Frame: ", self.video_coords[-1][0]," Ball: ", self.balls[pos])
                        self.balls[pos].add_point(self.video_coords[-1][0], current_pnt)
                        self.current_frame_objects.append(pos)
                    else:
                        if verbose:
                            print("New ball")
                        current_id = self.add_ball(self.video_coords[-1][0],current_pnt)
                        self.current_frame_objects.append(current_id)
                else:
                    if verbose:
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
            cv.line(clone, ball.pts[i-1][1], ball.pts[i][1], (0,128,255),3)
        return clone


    def prepare_json_for_this_video(self, verbose=False):
        sequences = []
        for pos in range(len(self.balls)): ##Creates marker sequence objects
            sequences.append( marker_sequence("", len(self.frames_objects), pos) ) 
        if verbose: 
            print("Number of sequences: ", len(sequences))
        for frame_num in range(len(self.frames_objects)):
            if verbose:
                print("---------------------")
                print("Frame number: ", frame_num + 1)
            for ball_object in range( len(self.balls) ):
                if verbose:
                    print("==== New Ball ====")
                    print("Ball iter", self.balls[ball_object].iter)
                    print("Ball ID: ", ball_object)
                    print("Current iter: ", self.balls[ball_object].iter)
                    print("Current iter pos: ", self.balls[ball_object].iter_pos)
                    
                if (frame_num + 1) < self.balls[ball_object].iter:
                    ## Need to assign a -1 here
                    if (verbose):
                        print("frame num < iter, therefore adding position of np.nan")
                    sequences[ball_object].set_coordinates(np.nan,np.nan, frame_num)
                elif (frame_num + 1) == self.balls[ball_object].iter:
                    ## Ball is in frame
                    iter_position = self.balls[ball_object].iter_pos
                    current_ball = self.balls[ball_object]
                    current_coords = current_ball.pts[iter_position][1]
                    sequences[ball_object].set_coordinates(current_coords[0],current_coords[1],frame_num)
                    ## Update iter value
                    self.balls[ball_object].iter_pos += 1
                    if self.balls[ball_object].iter_pos < len(current_ball.pts):
                        self.balls[ball_object].iter = current_ball.pts[self.balls[ball_object].iter_pos][0]
                elif (frame_num + 1) > self.balls[ball_object].iter:
                    ## Run out of ball objects, keep assigning -1
                    if (verbose):
                        print("frame num > iter, therefore adding position of np.nan")
                    sequences[ball_object].set_coordinates(np.nan,np.nan,frame_num)
        return sequences

    
def setup_analyse_video(video_path, video_name, video_format, location=os.path.join(os.getcwd(),".."), display=True):
    ssd = cv.dnn.readNetFromCaffe(os.path.join(location, 'detection/resources', 'MobileNetSSD_deploy.prototxt'),
                                  os.path.join(location, 'detection/resources', 'MobileNetSSD_deploy.caffemodel'))
    classifier = cv.dnn.readNetFromTensorflow(os.path.join(location, 'detection/resources/frozen_model_reshape_test.pb'))
    detector = cv.xfeatures2d.SURF_create(2000)
    detector.setUpright(True)

    nn = Trained_NN()
    analyse_path = Analyse_Path(display=display)
    analyse_path.classify(nn, video_path, video_name, video_format, ssd=ssd, detector=detector, flip=False, detect_classifier=classifier)
    return analyse_path.prepare_json_for_this_video()
    
def pickle_sequences(sequences, video_name):
    with open("pickle_files/sequences_" + video_name + '.pkl','wb') as f:
        pickle.dump(sequences,f)

def analyse_and_export(video_path, video_name, video_format, location, display):
    seq = setup_analyse_video(video_path, video_name, video_format, location, display)
    pickle_sequences(seq, video_name)


if __name__=='__main__':
    location = os.path.join(os.getcwd(),"..")
    video_name = "video_2_1"
    video_format = ".avi"
    vid_path = os.path.join(location,"tracking","resources",video_name+video_format)
    analyse_and_export(vid_path, video_name, video_format, location, True)
