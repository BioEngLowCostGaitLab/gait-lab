import os
import sys
functions_path = os.path.join(os.getcwd(),"..","detection")
sys.path.insert(0, functions_path)
from functions import generate_full_json_string
from analyse_video import setup_analyse_video
import json

def analyse_cameras(video_list, name, display):
    cameras = []
    for vid_path in video_list:
        vid_name = vid_path.split("\\")[-1]
        vid_format = "." + vid_name.split(".")[-1]
        vid_name = vid_name.split(".")[0]
        print("Name: {}\nFormat: {}\nPath: {}".format(vid_name, vid_format, vid_path))
        cameras.append(setup_analyse_video(vid_path, vid_name, vid_format, display=display))
    
    print("cameras generated, generating json...")
    full_string = generate_full_json_string(cameras, len(cameras), 149)
    print("dumping json")
    with open('json/'+name+'-2.json', 'w') as f:
        json.dump(full_string, f, indent=1)
    
if __name__=='__main__':
    vid_list = ['accuracy_resources\\gait_3_2\\video0.avi','accuracy_resources\\gait_3_2\\video1.avi']
    for i in range(len(vid_list)):
        vid_list[i] = os.path.join(os.getcwd(),vid_list[i])
    print("Analysing cameras")
    analyse_cameras(vid_list, name='acc_3_2', display=True)    
