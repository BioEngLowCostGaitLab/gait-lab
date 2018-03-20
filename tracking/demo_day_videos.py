from demo_day_analyse_video import analyse_and_export
import os

if __name__=="__main__":
    
    tracking_path = os.getcwd()
    video_names = ["video_1_1","video_1_2"]
    #video_names = ["video_2_1","video_2_2"]

    for i in range(len(video_names)):
        video_path = os.path.join(tracking_path,"resources",video_names[i] + ".avi")
        location = os.path.join(tracking_path,"..")
        
        print("Analysing: " + video_names[i])
        analyse_and_export(video_path, video_names[i], location,True)
        print("Video analysed and exported.\n")
    
    
