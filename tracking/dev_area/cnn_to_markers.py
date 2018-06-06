
# coding: utf-8

# In[1]:


import os
from os.path import join
import sys
import cv2 as cv
import numpy as np
from numpy.random import RandomState
import pickle
import matplotlib.pyplot as plt

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers
from keras import backend as K
from keras.callbacks import EarlyStopping, ModelCheckpoint


# In[2]:


def load_labels(specific_video=None):
    """ Loads in image data as numpy arrays """
    sequence = []
    none_count = 0 
    filedir = join(os.getcwd(),"labels")
    for file in os.listdir(filedir):
        ## change current seq when video_id change or marker number changes
        if file.endswith(".jpg"):
            file = file.split(".")[0]
            file = file.split("_")
            if specific_video == None:
                video_id, marker_num, marker_type, frame_num, x_pos, y_pos = file[0], int(file[1]), int(file[2]), int(file[3]), int(file[4]), int(file[5])
                current_seq = [video_id, marker_num, marker_type, frame_num, x_pos, y_pos]
                sequence.append(current_seq)
            else:
                if file[0] == video_id:
                    video_id, marker_num, marker_type, frame_num, x_pos, y_pos = file[0], int(file[1]), int(file[2]), int(file[3]), int(file[4]), int(file[5])
                    current_seq = [video_id, marker_num, marker_type, frame_num, x_pos, y_pos]#, dist]
                    sequence.append(current_seq)
    return sequence


# In[3]:


def sort_labels(sequence):
    sequence.sort(key=lambda x: x[3]) ## Sort by frame number
    sequence.sort(key=lambda x: x[1]) ## Sort by marker_num
    sequence.sort(key=lambda x: x[0]) ## Sort by video_name
    return sequence


# In[4]:


def assign_labels(sequence):
    ##  ball change or vid change
    prev_vid_id, prev_marker_num = sequence[0][0][0], sequence[0][0][1]
    for idx, seq in enumerate(sequence):
        vid_id, marker_num = seq[0], seq[1]
        if (vid_id != prev_vid_id) or (marker_num != prev_marker_num):
            prev_vid_id, prev_marker_num = vid_id, marker_num
            prev_coords, prev_frame_num = np.array([-1,-1]), -1
        frame_num, x_pos, y_pos = seq[3], seq[4], seq[5]
        current_coords = np.array([x_pos, y_pos])
        if (prev_coords[0] == -1) & (prev_coords[1] == -1):
            dist = -1
        else:
            dist = np.linalg.norm(current_coords - prev_coords)
        if (prev_frame_num == -1):
            frame_diff = -1
        else:
            frame_diff = frame_num - prev_frame_num
        prev_coords = current_coords
        prev_frame_num = frame_num
        sequence[idx].append(dist)
        sequence[idx].append(frame_diff)
    return sequence


# In[5]:


def load_video(video_path, video_name, flip, display = False): ## Convert 3rd element in video name into flip
    width, height = 960, 540
    cap = cv.VideoCapture(join(video_path,video_name))
    ret, frame = cap.read()
    if (flip):
        frame = cv.flip(frame, 0)
    clone = cv.resize(frame, (width,height))
    if (display):
        cv.namedWindow("Video")
    frame_num = 0
    frames = []
    while (ret):
        if (display):
            cv.imshow("Video", clone)
        frames.append( [frame, frame_num] )
        if (display):
            key = cv.waitKey(0)
            if key == 113:
                break
        ret, frame = cap.read()
        if (ret):
            frame_num += 1
            if (flip):
                frame = cv.flip(frame, 0)
            clone = cv.resize(frame, (width, height))
    cap.release()
    if (display):
        cv.destroyAllWindows()
    return frames


# In[6]:


def load_data_and_labels(sequence, vid_format=".avi"):
    print("Loading videos")
    filedir = join(os.getcwd(),"resources")
    video_recorded = []
    for file in os.listdir(filedir):
        video_id = file.split(".")[0]
        video_recorded.append(video_id)
    video_annotated = list(sorted(set([i[0] for i in sequence])))
    video_data = []
    """ Checking the videos annotated is in the video recorded """
    for rec in video_recorded:
        if rec in video_annotated:
            data = []
            print("Found: {}".format(rec))
            labels = [i for i in seq if i[0] == rec]
            labels.sort(key=lambda x: x[3]) ## Sort by frame number
            labels = np.asarray(labels)[:,1:].astype('float32')
            frames = load_video(filedir, rec + vid_format, False)
            prev_frame = 0
            frame_labels = []
            for idx, label in enumerate(labels):
                curr_frame = int(label[2])
                if (curr_frame != prev_frame):
                    data.append([frames[prev_frame][0], frame_labels])                    
                    frame_labels = [label]
                elif idx == len(labels) - 1:
                    frame_labels.append(label)
                    data.append([frames[curr_frame][0],frame_labels])
                else:
                    frame_labels.append(label)
                prev_frame = int(curr_frame)
            video_data.append(data)
    print("Search Complete")
    return video_data    


# In[7]:


def data_to_np(data):
    data_np = np.asarray(data)

    x_values = []
    y_values = []
    for i in range(len(data_np[:,:,0])):
        x_np = data_np[:,:,0][i]
        x_shape = list(x_np[0].shape)
        x_shape[:0] = [len(x_np)]
        x_np = np.concatenate(x_np).reshape(x_shape)
        x_values.append(x_np)
        
        y_np = data_np[:,:,1][i]
        y_frames = []
        for frame_y in y_np:
            frame_y = np.asarray(frame_y)
            zero_np = np.zeros((16,7))
            zero_np[:frame_y.shape[0],:frame_y.shape[1]] = frame_y
            y_frames.append(zero_np)
        y_values.append(y_frames)
        
    x_img = np.asarray(x_values)
    y_values = np.asarray(y_values)
    x_diff = y_values[:, :, :, 5:]
    y_cords = y_values[:, :, :, 3:5]
    print("x_img shape: {}, x_diff shape: {}, y_values shape: {}".format(x_img.shape, x_diff.shape, y_cords.shape))
    return x_img, x_diff, y_cords


# In[8]:


def normalise_img(x_values):
    return x_values / 255


# In[9]:


seq = load_labels()
seq = sort_labels(seq)
seq = assign_labels(seq)
data = load_data_and_labels(seq)
x_img, x_diff, y = data_to_np(data)


# In[10]:


# need to normalise y values
# need to build a model that includes distance and frame diff
# model predicting x and y values

# going to build model that predicts coords from image


# In[11]:


def cnn_prepare(x_value, y_value):
    x_val = np.reshape(x_value,(x_value.shape[0] * x_value.shape[1], 
                                x_value.shape[2], 
                                x_value.shape[3], 
                                x_value.shape[4]))
    y_val = np.reshape(y_value,(y_value.shape[0] * y_value.shape[1], 
                                y_value.shape[2] * y_value.shape[3]))
    return x_val, y_val


# In[12]:


def split_np(x_data, y_data, percent):
    """ splits a numpy array into testing and training """
    position = int(len(x_data) * (1-percent))
    x_train, x_test = x_data[:position], x_data[position:]
    y_train, y_test = y_data[:position], y_data[position:]
    return x_train, y_train, x_test, y_test


# In[13]:


x_cnn, y_cnn = cnn_prepare(x_img, y)
x_train, y_train, x_test, y_test = split_np(x_cnn, y_cnn, 0.2)


# In[14]:


print('x_train shape: {}, x_test shape: {}'.format(x_train.shape,x_test.shape))
print('y_train shape: {}, y_test shape: {}'.format(y_train.shape,y_test.shape))


# In[15]:


input_shape = x_train.shape[1:]
output_shape = y_train.shape[1]

model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3),
                activation='relu',
                input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(output_shape))
model.compile(loss='mean_squared_error', 
              optimizer='adam',
              metrics=['accuracy'])


# In[ ]:


monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=5, verbose=1, mode='auto')
checkpointer = ModelCheckpoint(filepath="dnn/tmp_best_weights.hdf5", verbose=0, save_best_only=True) # save best model

batch_size = 128
epochs = 1000
import time
start_time = time.time()

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test),
          callbacks=[monitor,checkpointer])
model.load_weights('dnn/tmp_best_weights.hdf5') # load weights from best model


save_dir = join(os.getcwd(),"dnn")
save_path = join(save_dir,str(int(start_time)) + "_cnn.h5")
model.save(save_path)

score = model.evaluate(x_test, y_test, verbose=2)
print('Test loss: {}'.format(score[0]))
print('Test accuracy: {}'.format(score[1]))

elapsed_time = time.time() - start_time
print("Elapsed time: {}".format(hms_string(elapsed_time)))

