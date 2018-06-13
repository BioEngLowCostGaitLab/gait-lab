import os
from os.path import join
import cv2 as cv
  
def read_images(save_path, load_path, width=1280, height=720, flip=True, verbose=False):
    frame_names = []
    for file in os.listdir(load_path):
        file_id = file.split(".")[0]
        frame = int(file_id.split("_")[2])
        frame_names.append([file,frame])
    frame_names.sort(key=lambda x: x[1])
    out_video = cv.VideoWriter(save_path, -1, 30.0, (width,height) )
    for j in frame_names:
        img = cv.imread(join(load_path, j[0]))
        print(j[1])
        out_video.write(img)
    cv.destroyAllWindows()
    out_video.release()
    print("Completed.\nVideo file name: {}\nStored at: {}".format(save_name,save_path))
    
if __name__=='__main__':
    
    for i in range(2):
        print(i)
        vid_num = str(i)
        folder_name = "vid_"+vid_num
        load_path = join(os.getcwd(), folder_name)
        save_name, save_format = "video"+vid_num, ".avi"
        save_path = join(os.getcwd(), "..", "gait_2_3", save_name + save_format)
        read_images(save_path, load_path)
        print("Save path: {}".format(save_path))
        print("Load path: {}".format(load_path))



