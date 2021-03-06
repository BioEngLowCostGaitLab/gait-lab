import os
from os.path import join
import sys
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

# Nicely formatted time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

import pickle

print("loading data...")

data = pickle.load(open("data_rand.p","rb"))

print("data loaded")

x_train, y_train, x_test, y_test = data[0], data[1], data[2], data[3]

print("building model")

input_shape = x_train.shape[1:]
output_shape = y_train.shape[1]

model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3),
                activation='relu',
                input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(64, (3, 3),activation='relu'))
model.add(Conv2D(128, (3, 3),activation='relu'))
model.add(MaxPooling2D((2,2), strides=(2,2)))
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

print("model built")

monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=20, verbose=1, mode='auto')
checkpointer = ModelCheckpoint(filepath="dnn/tmp_best_weights.hdf5", verbose=0, save_best_only=True) # save best model

print("load weights")

model.load_weights('dnn/tmp_best_weights-1.hdf5')

print("training model")

batch_size = 32
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

