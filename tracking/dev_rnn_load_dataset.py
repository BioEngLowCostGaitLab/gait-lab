import cv2 as cv
import numpy as np
import os
from os.path import join
from numpy.random import RandomState
import tensorflow as tf
from tensorflow.contrib.data import Dataset, Iterator

def pad(arr):
    r = np.zeros((24,24,3))
    r[:arr.shape[0],:arr.shape[1],:arr.shape[2]] = arr
    return r

def load_labels(randomise=True, verbose=False):
    fdir = "labels"
    x_values = []
    y_values = []
    x = 0
    none_count = 0   
    for file in os.listdir(fdir):
        if file.endswith(".jpg"):
            img = cv.imread(os.path.join(fdir,file), cv.IMREAD_UNCHANGED)
            if not img is None:
                x_values.append( os.path.join(fdir,file))
##                x_values.append(fdir + "/" + file)
                if int(file[0]) == 0:    
                    y_values.append(0)
                else:
                    y_values.append(1)               
            else:
                none_count += 1
            x += 1
    if (verbose):
        print("None count: ", none_count)
    x_np = np.array(x_values)
    y_np = np.array(y_values)
    if (randomise):
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



x_np, y_np = load_labels()

train_imgs, train_labels, val_imgs, val_labels = split_np(x_np, y_np, 0.998)

train_imgs = tf.constant(train_imgs)
train_labels = tf.constant(train_labels)
val_imgs = tf.constant(val_imgs)
val_labels = tf.constant(val_labels)

tr_data = tf.data.Dataset.from_tensor_slices( (train_imgs,train_labels) )
val_data = tf.data.Dataset.from_tensor_slices( (val_imgs,val_labels) )

iterator = Iterator.from_structure(tr_data.output_types, tr_data.output_shapes)

next_element = iterator.get_next()

training_init_op = iterator.make_initializer(tr_data)
validation_init_op = iterator.make_initializer(val_data)


batch_size = 20
NUM_CLASSES = 2

def input_parser(img_path, label):
    one_hot = tf.one_hot(label, NUM_CLASSES)

    img_file = tf.read_file(img_path)
    img_decoded = tf.image.decode_image(img_file, channels=3)

    return img_decoded, one_hot



print(tr_data)
tr_data = tr_data.map(input_parser)
print(tr_data)
tr_data = tr_data.batch(batch_size)
print(tr_data)

tmp = tr_data.make_one_shot_iterator().get_next()
print(tmp)










print("\n===============================\n")

with tf.Session() as sess:
    sess.run(training_init_op)
    while True:
        try:
            elem = sess.run(next_element)
            print(elem)
        except tf.errors.OutOfRangeError:
            print("\nEnd of training dataset")
            break









