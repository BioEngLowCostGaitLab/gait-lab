import cv2 as cv
import numpy as np
import os
from os.path import join
from numpy.random import RandomState

def pad(arr):
    r = np.zeros((24,24,3))
    r[:arr.shape[0],:arr.shape[1],:arr.shape[2]] = arr
    return r

def load_labels(randomise=True):
    fdir = "labels"
    x_values = []
    y_values = []
    x = 0
    none_count = 0   
    for file in os.listdir(fdir):
        if file.endswith(".jpg"):
            img = cv.imread(os.path.join(fdir,file), cv.IMREAD_UNCHANGED)
            if not img is None:
                img = pad(img)
                x_values.append(img)
                if int(file[0]) == 0:    
                    y_values.append([0,1])
                else:
                    y_values.append([1,0])               
            else:
                none_count += 1
            x += 1
    print("None count: ", none_count)
    shape = list(x_values[0].shape)
    shape[:0] = [len(x_values)]
    x_np = np.concatenate(x_values).reshape(shape)
    y_np = np.array(y_values)
    x_np, y_np = random_np(x_np, y_np)
    return x_np, y_np

def random_np(x_np, y_np):
    prng = RandomState(0)
    randomise = prng.permutation(x_np.shape[0])
    x_np = x_np[randomise]
    y_np = y_np[randomise]
    return x_np, y_np
    
def split_np(x_data, y_data, percent):
    position = int(len(x_data) * (1-percent))
    x_train = x_data[:position]
    x_test = x_data[position:]
    y_train = y_data[:position]
    y_test = y_data[position:]
    return x_train, y_train, x_test, y_test
