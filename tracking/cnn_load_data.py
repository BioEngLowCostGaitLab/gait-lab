import cv2 as cv
import numpy as np
import os
from os.path import join

def pad(arr):
    r = np.zeros((24,24,3))
    r[:arr.shape[0],:arr.shape[1],:arr.shape[2]] = arr
    return r

def load_labels():
    fdir = "labels"
    dataset = []
    x = 0
    none_count = 0
    for file in os.listdir(fdir):
        if file.endswith(".jpg"):
            img = cv.imread(os.path.join(fdir,file), cv.IMREAD_UNCHANGED)
            if not img is None:
                img = pad(img)
                if int(file[0]) == 0:    
                    dataset.append([img,np.array([0,1])])
                else:
                    dataset.append([img,np.array([1,0])])
            else:
                none_count += 1
            x += 1
    print("None count: ", none_count)
    return np.array(dataset)

