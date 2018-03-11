import sys
functions_path = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection'
sys.path.insert(0, functions_path)
from functions import analyse
import tensorflow as tf
import cv2 as cv
import numpy as np
import os
from os.path import join
import matplotlib.pyplot as plt
from functions import analyse
from datetime import datetime as dt
########from cnn_load_data import load_labels as old_load_labels
from load_training_data_test import load_labels, split_np

class rnnClassify:
    def __init__(self, n_classes=2, hm_epochs=25, keep_rate=0.8):
        tf.reset_default_graph()
        self.n_classes = n_classes
        self.hm_epochs = hm_epochs
        self.keep_rate = keep_rate
        self.keep_prob = tf.placeholder(tf.float32)
        # Weight variables and input placeholders
        self.x = tf.placeholder(tf.float32, [None,24, 24, 3])
        self.y = tf.placeholder(tf.float32, [None,2])
        self.weights = {'W_conv1':tf.Variable(tf.random_normal([5,5,3,32]),name='W_conv1'),
                        'W_conv2':tf.Variable(tf.random_normal([5,5,32,64]),name='W_conv2'),
                        'W_fc':tf.Variable(tf.random_normal([6*6*64, 1024]),name='W_fc'),
                        'W_out':tf.Variable(tf.random_normal([1024, self.n_classes]),name='W_out')}
        self.biases = {'b_conv1':tf.Variable(tf.random_normal([32]),name='b_conv1'),
                       'b_conv2':tf.Variable(tf.random_normal([64]),name='b_conv2'),
                       'b_fc':tf.Variable(tf.random_normal([1024]),name='b_fc'),
                       'b_out':tf.Variable(tf.random_normal([self.n_classes]),name='b_out')}
        # Cost optimizer
        self.model = self.rnn_model()
        self.cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.model, labels=self.y) )
        self.train_op = tf.train.AdamOptimizer().minimize(self.cost)
        # Auxiliary ops
        self.saver = tf.train.Saver()
        
    def frame_stamp(self):
        current = dt.now()
        out_str = (str(current.year) + str(current.month) + str(current.day) + "_" + 
                   str(current.hour) + str(current.minute) + str(current.second) + "_" +
                   str(current.microsecond))
        return out_str

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
    
    def rnn_load_data(self):
        x_np, y_np = load_labels()
        self.train_data_x, self.train_data_y, self.test_data_x, self.test_data_y = split_np(x_np, y_np, 0.25)
        print("Traing_data count: ", len(self.train_data_x))
        print("Test_data count: ", len(self.test_data_x))
        
    def rnn_model(self):
        # 5 x 5, 3 input, produces 32 features
        x_tf = tf.reshape(self.x, shape=[-1,24,24,3])
        conv1 = self.maxpool2d(self.conv2d(x_tf, self.weights['W_conv1'], self.biases['b_conv1']))
        conv2 = self.maxpool2d(self.conv2d(conv1, self.weights['W_conv2'], self.biases['b_conv2']))
        fc = tf.reshape(conv2,[-1,6*6*64])
        fc = tf.nn.relu(tf.matmul(fc, self.weights['W_fc']) + self.biases['b_fc'])
        fc = tf.nn.dropout(fc, self.keep_rate)
        output = tf.matmul(fc, self.weights['W_out']) + self.biases['b_out']
        return output
    
    def rnn_train(self, zero_catch=0):    
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            sess.run(tf.global_variables_initializer())
            self.loss_plot = []
            hm_zeros = 0
            for epoch in range(self.hm_epochs):
                c = 0
                _, c_tmp = sess.run([self.train_op, self.cost], feed_dict = {self.x: self.train_data_x, self.y: self.train_data_y})
                c += c_tmp
                self.loss_plot.append(c)
                print('Epoch: ', epoch + 1, ' completed out of: ', self.hm_epochs, ' loss: ', c)
                if (zero_catch > 0) and (c == 0):
                    hm_zeros += 1
                    if hm_zeros == zero_catch:
                        print("Reached zero catch of: ", zero_catch)
                        break
                elif (c != 0):
                    hm_zeros = 0  
            location = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Python/EDP/rnn_model/'
            save_path = self.saver.save(sess, location + "current_model.ckpt")
            print("Model saved in path: %s" % save_path)
    
    def rnn_test(self):
        # Check how good model is
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            location = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Python/EDP/rnn_model/'
            self.saver.restore(sess, location + "current_model.ckpt")
            cumm_acc = tp=tn=fp=fn = 0
            length = len(self.test_data_x)
            output = sess.run(self.rnn_model(), feed_dict={self.x: self.test_data_x})
            curr_result = 0
            true_result = self.test_data_y.argmax(axis=0)
            output_result = output.argmax(axis=1)
            true_result = self.test_data_y.argmax(axis=1)
            accuracy = output_result + true_result
            ac = ((accuracy == 0) | (accuracy == 2))
            print(np.sum(ac)/len(ac))
        
    def rnn_predict(self, predict_data_x):
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            location = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Python/EDP/rnn_model/'
            self.saver.restore(sess, location + "current_model.ckpt")
            acc = true_pos = true_neg = false_pos = false_neg = 0
            if (type(predict_data_x[0][0][0]).__name__ == 'float64'):
                output = sess.run(self.rnn_model(), feed_dict={self.x: predict_data_x})
                return output
            elif (type(predict_data_x[0][0][0][0]).__name__ == 'float64'):
                output = []
                length = len(self.test_data_x)
                for i in range(length):
                    if (i % 25 == 0): print(i/length * 100)
                    output.append(sess.run(self.rnn_model(), feed_dict={self.x: predict_data_x[i]}))
                return output


if __name__ == '__main__':
    print('-- Loading Data --')
    predictor = rnnClassify(hm_epochs=100)
    predictor.rnn_load_data()
    print('-- Training --')
    predictor.rnn_train(zero_catch=2)
    print('-- Testing --')
    predictor.rnn_test()



