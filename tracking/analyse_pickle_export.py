from analyse_video import analyse_and_pickle
from plot_path import export_video
import os

if __name__=="__main__":
    
    tracking_path = os.getcwd()
    video_name = "video_1_1"
    video_path = os.path.join(tracking_path,"resources",video_name + ".avi")
    location = os.path.join(tracking_path,"..")
    
    print("Analysing: " + video_name)
    #analyse_and_pickle(video_path, video_name, location,True)

    #print("Video analysed and pickled.")
    ##print("===============")
    ##print("Exporting video with path")

    ##Has an issue where everything is nan, needs to be fixed.
    ##export_video(video_path, video_name, tracking_path, flip=False)  

    ##print("Video exported.")
    
    
