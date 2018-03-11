import tensorflow as tf
import cv2 as cv
import numpy as np

class Trained_NN:
    def __init__(self, n_classes=2, keep_rate=0.8):
        tf.reset_default_graph()
        self.n_classes = n_classes
        self.keep_rate = keep_rate
        
        self.x = tf.placeholder(tf.float32, [None, 24, 24, 3])
        self.y = tf.placeholder(tf.float32, [None, n_classes])
        self.weights = {'W_conv1':tf.Variable(tf.random_normal([5,5,3,32]),name='W_conv1'),
                        'W_conv2':tf.Variable(tf.random_normal([5,5,32,64]),name='W_conv2'),
                        'W_fc':tf.Variable(tf.random_normal([6*6*64, 1024]),name='W_fc'),
                        'W_out':tf.Variable(tf.random_normal([1024, self.n_classes]),name='W_out')}
        self.biases = {'b_conv1':tf.Variable(tf.random_normal([32]),name='b_conv1'),
                       'b_conv2':tf.Variable(tf.random_normal([64]),name='b_conv2'),
                       'b_fc':tf.Variable(tf.random_normal([1024]),name='b_fc'),
                       'b_out':tf.Variable(tf.random_normal([self.n_classes]),name='b_out')}
        
        self.model = self.nn_model()
        self.saver = tf.train.Saver()
        
    def conv2d(self, tf_in, W, b):
        conv = tf.nn.conv2d(tf_in, W, strides=[1,1,1,1], padding='SAME')
        conv_with_b = tf.nn.bias_add(conv, b)
        conv_out = tf.nn.relu(conv_with_b)
        return conv_out

    def maxpool2d(self,tf_in):
        return tf.nn.max_pool(tf_in, ksize=[1,2,2,1], strides=[1,2,2,1],padding='SAME')
    
    def nn_model(self):
        x_tf = tf.reshape(self.x, shape=[-1,24,24,3])
        conv1 = self.maxpool2d(self.conv2d(x_tf, self.weights['W_conv1'], self.biases['b_conv1']))
        conv2 = self.maxpool2d(self.conv2d(conv1, self.weights['W_conv2'], self.biases['b_conv2']))
        fc = tf.reshape(conv2,[-1,6*6*64])
        fc = tf.nn.relu(tf.matmul(fc, self.weights['W_fc']) + self.biases['b_fc'])
        fc = tf.nn.dropout(fc, self.keep_rate)
        output = tf.matmul(fc, self.weights['W_out']) + self.biases['b_out']
        return output
      
    def nn_predict(self, predict_data_x):
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            location = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/tracking/saved_model/'
            self.saver.restore(sess, location + "ball_model.ckpt")
            output = sess.run(self.nn_model(), feed_dict={self.x: predict_data_x})
            output = output.argmax(axis=1)
            return output

#=======================================================================================================#

if __name__ == '__main__':
    predictor = Trained_NN()
    
    
