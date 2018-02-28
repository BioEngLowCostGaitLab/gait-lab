import sys
functions_path = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/detection'
sys.path.insert(0, functions_path)
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from load_training_data import load_labels, split_np

class rnnClassify:
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
        self.model = self.rnn_model(self.x)
        self.cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=self.model, labels=self.y) )
        self.train_op = tf.train.AdamOptimizer().minimize(self.cost)
        # Auxiliary ops
        self.saver = tf.train.Saver()

    #=================================================================================#

    def conv2d(self, tf_in, W, b):
        conv = tf.nn.conv2d(tf_in, W, strides=[1,1,1,1], padding='SAME')
        conv_with_b = tf.nn.bias_add(conv, b)
        conv_out = tf.nn.relu(conv_with_b)
        return conv_out

    def maxpool2d(self,tf_in):
        return tf.nn.max_pool(tf_in, ksize=[1,2,2,1], strides=[1,2,2,1],padding='SAME')

    #=================================================================================#
    
    def rnn_load_data(self):
        x_dataset, y_dataset = old_load_labels()
        x_train, y_train, x_test, y_test = split_np(x_dataset, y_dataset, 0.25)
        
    def rnn_model(self, x_in):
        x_tf = tf.reshape(x_in, shape=[-1,24,24,3])
        conv1 = self.maxpool2d(self.conv2d(x_tf, self.weights['W_conv1'], self.biases['b_conv1']))
        conv2 = self.maxpool2d(self.conv2d(conv1, self.weights['W_conv2'], self.biases['b_conv2']))
        fc = tf.reshape(conv2,[-1,6*6*64])
        fc = tf.nn.relu(tf.matmul(fc, self.weights['W_fc']) + self.biases['b_fc'])
        fc = tf.nn.dropout(fc, self.keep_rate)
        output = tf.matmul(fc, self.weights['W_out']) + self.biases['b_out']
        return output
    
    def rnn_train(self):    
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            sess.run(tf.global_variables_initializer())
            self.loss_plot = []
            hm_zeros = 0
            for epoch in range(self.hm_epochs):
                c = 0
                for i in range(len(self.train_data_x)):
                    _, c_tmp = sess.run([self.train_op, self.cost], feed_dict = {self.x: self.train_data_x,
                                                                                 self.y: self.train_data_y})
                    c += c_tmp
                self.loss_plot.append(c)
                print('Epoch: ', epoch, ' completed out of: ', self.hm_epochs, ' loss: ', c)
            location = './saved_model/'
            save_path = self.saver.save(sess, location + "dev_model.ckpt")
            print("Model saved in path: %s" % save_path)
    

if __name__ == '__main__':
    predictor = rnnClassify(hm_epochs=50)
    predictor.rnn_load_data()
    print('-------')
    predictor.rnn_train()

    