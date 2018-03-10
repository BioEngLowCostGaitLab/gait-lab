import sys
functions_path = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection'
sys.path.insert(0, functions_path)
from functions import analyse
import tensorflow as tf
import cv2 as cv
import numpy as np
import os
from os.path import join
from datetime import datetime as dt
from load_training_data import load_labels

class run_cnn:
    def __init__(self, n_classes=1, hm_epochs=25, keep_rate=0.8):
        tf.reset_default_graph()
        self.n_classes = n_classes
        self.hm_epochs = hm_epochs
        self.keep_rate = keep_rate
        
        # Weight variables and input placeholders
        self.x = tf.placeholder(tf.float32, [None,24, 24, 3])
        self.y = tf.placeholder(tf.float32, [None,n_classes])
        self.weights = {'W_conv1':tf.Variable(tf.random_normal([5,5,3,32]),name='W_conv1'),
                        'W_conv2':tf.Variable(tf.random_normal([5,5,32,64]),name='W_conv2'),
                        'W_fc':tf.Variable(tf.random_normal([6*6*64, 1024]),name='W_fc'),
                        'W_out':tf.Variable(tf.random_normal([1024, self.n_classes]),name='W_out')}
        self.biases = {'b_conv1':tf.Variable(tf.random_normal([32]),name='b_conv1'),
                       'b_conv2':tf.Variable(tf.random_normal([64]),name='b_conv2'),
                       'b_fc':tf.Variable(tf.random_normal([1024]),name='b_fc'),
                       'b_out':tf.Variable(tf.random_normal([self.n_classes]),name='b_out')}
        
        # Cost optimizer
        self.model = self.cnn_model(self.x)


    def pad(self, arr):
        r = np.zeros((24,24,3))
        r[:arr.shape[0],:arr.shape[1],:arr.shape[2]] = arr
        return r
          
    def conv2d(self, tf_in, W, b):
        conv = tf.nn.conv2d(tf_in, W, strides=[1,1,1,1], padding='SAME')
        conv_with_b = tf.nn.bias_add(conv, b)
        conv_out = tf.nn.relu(conv_with_b)
        return conv_out

    def maxpool2d(self,tf_in):
        return tf.nn.max_pool(tf_in, ksize=[1,2,2,1], strides=[1,2,2,1],padding='SAME')
        
    def cnn_model(self, x_in):
        # 5 x 5, 3 input, produces 32 features
        x_tf = tf.reshape(x_in, shape=[-1,24,24,3])
        conv1 = self.maxpool2d(self.conv2d(x_tf, self.weights['W_conv1'], self.biases['b_conv1']))
        conv2 = self.maxpool2d(self.conv2d(conv1, self.weights['W_conv2'], self.biases['b_conv2']))
        fc = tf.reshape(conv2,[-1,6*6*64])
        fc = tf.nn.relu(tf.matmul(fc, self.weights['W_fc']) + self.biases['b_fc'])
        fc = tf.nn.dropout(fc, self.keep_rate)
        output = tf.matmul(fc, self.weights['W_out']) + self.biases['b_out']
        return output
      
    def cnn_predict(self, predict_data_x):
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            location = './saved_model/'
            self.saver.restore(sess, location + "current_model.ckpt")
            print("Model restored")
            print("---------------------------------------")
            acc = true_pos = true_neg = false_pos = false_neg = 0
            if (type(predict_data_x[0][0][0]).__name__ == 'float64'):
                output = sess.run(self.cnn_model(), feed_dict={self.x: predict_data_x})
                return output
            elif (type(predict_data_x[0][0][0][0]).__name__ == 'float64'):
                output = []
                length = len(self.test_data_x)
                for i in range(length):
                    if (i % 50 == 0): print("Progress: ", i/length * 100)
                    output.append(sess.run(self.cnn_model(), feed_dict={self.x: predict_data_x[i]}))
                return output


if __name__ == '__main__':
    predictor = run_cnn(hm_epochs=50)
    
    
