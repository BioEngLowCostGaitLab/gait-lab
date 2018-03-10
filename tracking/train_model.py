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
from datetime import datetime as dt
from load_training_data import load_labels, split_np

class train_cnn:
    def __init__(self, n_classes=1, hm_epochs=25, train_split=0.5, keep_rate=0.8):
        tf.reset_default_graph()
        self.n_classes = n_classes
        self.hm_epochs = hm_epochs
        self.train_split = train_split
        self.keep_rate = keep_rate
        # Weight variables and input placeholders
        self.x = tf.placeholder(tf.float32, [24, 24, 3])
        self.y = tf.placeholder(tf.float32, [n_classes])
        self.weights = {'W_conv1':tf.Variable(tf.random_normal([5,5,3,32]),name='W_conv1'),
                        'W_conv2':tf.Variable(tf.random_normal([5,5,32,64]),name='W_conv2'),
                        'W_fc':tf.Variable(tf.random_normal([6*6*64, 1024]),name='W_fc'),
                        'W_out':tf.Variable(tf.random_normal([1024, self.n_classes]),name='W_out')}
        self.biases = {'b_conv1':tf.Variable(tf.random_normal([32]),name='b_conv1'),
                       'b_conv2':tf.Variable(tf.random_normal([64]),name='b_conv2'),
                       'b_fc':tf.Variable(tf.random_normal([1024]),name='b_fc'),
                       'b_out':tf.Variable(tf.random_normal([self.n_classes]),name='b_out')}
        
        # Cost optimizer
        self.model = self.cnn_model()
        self.cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.model, labels=self.y) )
        self.train_op = tf.train.AdamOptimizer().minimize(self.cost)
        
        # Auxiliary ops
        self.saver = tf.train.Saver()

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
    
    def cnn_load_data(self):
        x_np, y_np = load_labels()
        self.train_imgs, self.train_labels, self.test_imgs, self.test_labels = split_np(x_np, y_np, self.train_split)
        print("Traing_data count: ", len(self.train_imgs))
        print("Test_data count: ", len(self.test_imgs))
        
    def cnn_model(self):
        # 5 x 5, 3 input, produces 32 features
        x_tf = tf.reshape(self.x, shape=[-1,24,24,3])
        conv1 = self.maxpool2d(self.conv2d(x_tf, self.weights['W_conv1'], self.biases['b_conv1']))
        conv2 = self.maxpool2d(self.conv2d(conv1, self.weights['W_conv2'], self.biases['b_conv2']))
        fc = tf.reshape(conv2,[-1,6*6*64])
        fc = tf.nn.relu(tf.matmul(fc, self.weights['W_fc']) + self.biases['b_fc'])
        fc = tf.nn.dropout(fc, self.keep_rate)
        output = tf.matmul(fc, self.weights['W_out']) + self.biases['b_out']
        return output
    
    def cnn_train(self, zero_catch=0):
        print(type(self.train_imgs))
        print(type(self.train_labels))
        print(self.train_imgs.shape)
        print(self.train_labels.shape)
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            sess.run(tf.global_variables_initializer())
            self.loss_plot = []
            hm_zeros = 0
            for epoch in range(self.hm_epochs):
                c = 0
                for i in range(len(self.train_imgs)):
        
                    _, c_tmp = sess.run([self.train_op, self.cost], feed_dict = {self.x: self.train_imgs[i],
                                                                                 self.y: self.train_labels[i]})
                    c += c_tmp
                self.loss_plot.append(c)
                print('Epoch: ', epoch, ' completed out of: ', self.hm_epochs, ' loss: ', c)
                if (zero_catch > 0) and (c == 0):
                    hm_zeros += 1
                    if hm_zeros == zero_catch:
                        print("Reached zero catch of: ", zero_catch)
                        break
                elif (c != 0):
                    hm_zeros = 0  
            location = './saved_model/'
            save_path = self.saver.save(sess, location + "current_model.ckpt")
            print("Model saved in path: %s" % save_path)
    
    def calculate_accuracy(self, cumm_acc, curr_result, true_result, tp,tn,fp,fn):
        if true_result == 1 and curr_result == 0:
            fn += 1
        elif true_result == 0 and curr_result == 0:
            fp += 1
        elif true_result == 1 and curr_result == 1:
            tp += 1
        elif true_result == 0 and curr_result == 1:
            tn += 1
        cumm_acc += curr_result
        return cumm_acc, tp,tn,fp,fn
    
    def print_accuracy(self, length, cumm_acc, tp,tn,fp,fn):
        print("=======================================")
        print("Accuracy: ", cumm_acc/length*100)
        print("Tests: ", length)
        print("Positive Sample: ", tp + fn)
        print("Negative Sample: ", fp + tn)
        print("Incorrect: ", fp + fn)
        print("---------------------------------------")
        print("False Positives: ", fp)
        print("False Negatives: ", fn)
        print("True  Positives: ", tp)
        print("True  Negatives: ", tn)
        print("=======================================")
        plt.plot(self.loss_plot)
        plt.show()
    
    def cnn_test(self):
        # Check how good model is
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            location = './saved_model/'
            self.saver.restore(sess, location + "current_model.ckpt")
            print("Model restored")
            print("---------------------------------------")
            cumm_acc = tp=tn=fp=fn = 0
            length = len(self.test_imgs)
            for i in range(length):
                output = sess.run(self.cnn_model(), feed_dict={self.x: self.test_imgs[i]})
                curr_result = 0
                true_result = self.test_labels[i].argmax(axis=0)
                if (output.argmax(axis=1)[0] == self.test_labels[i].argmax(axis=0) ): curr_result = 1
                cumm_acc,tp,tn,fp,fn = self.calculate_accuracy(cumm_acc, curr_result, true_result, tp,tn,fp,fn)
            self.print_accuracy(length, cumm_acc, tp,tn,fp,fn)

if __name__ == '__main__':
    predictor = train_cnn(hm_epochs=50)
    predictor.cnn_load_data()
    print('-------')
    predictor.cnn_train(zero_catch=2)
    print('-------')
    predictor.cnn_test()
    print('-------')
    input('Enter to end...')
    
