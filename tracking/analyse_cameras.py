import sys
functions_path = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection'
sys.path.insert(0, functions_path)
from functions import generate_full_json_string
from analyse_video import analyse_video
import json

def analyse_cameras(video_list, name='test', display=False):
    cameras = []
    for i in video_list:
        cameras.append(analyse_video(i,display))

    full_string = generate_full_json_string(cameras, len(cameras))

    with open('json/'+name+'.json', 'w') as f:
        json.dump(full_string, f, indent=1)
    
if __name__=='__main__':
    vid_list = ['tracking/resources/video2/video0.mp4','tracking/resources/video2/video1.mp4']
    analyse_cameras(vid_list,display=True)    
