from analyse_video import analyse_and_pickle
from plot_path import export_video
import os

if __name__=="__main__":
    tracking_path = os.getcwd()
    video_name = "video_1_1"
    video_path = os.path.join(tracking_path,"resources",video_name + ".avi")
    location = os.path.join(tracking_path,"..")
    
    analyse_and_pickle(video_path, video_name, location, True)

    print("ANALYSED AND PICKLED")

    export_video(video_path, video_name, tracking_path)

    print("EXPORTED VIDEO")
    
    
