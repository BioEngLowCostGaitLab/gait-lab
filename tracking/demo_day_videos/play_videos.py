import os
import cv2 as cv

def play_videos(videos, window_title):
    cap = [cv.VideoCapture(i) for i in videos]

    frames = [None] * len(videos);
    ret = [None] * len(videos);

    while True:
        for i,c in enumerate(cap):
            if c is not None:
                ret[i], frames[i] = c.read();

        for i,f in enumerate(frames):
            if ret[i] is True:
                cv.imshow(window_title[i], frames[i]);
            else:
                cap = [cv.VideoCapture(i) for i in videos]

                frames = [None] * len(videos);
                ret = [None] * len(videos);
                

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    for c in cap:
        if c is not None:
            c.release();

    cv.destroyAllWindows()
    
if __name__=='__main__':
    videos = ['video_1_1.avi','video_1_2.avi']
    window_title = ['Lunge Side', 'Lunge 45 degrees']
    
    play_videos(videos, window_title)

    
    
