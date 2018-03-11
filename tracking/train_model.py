import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from load_data import load_labels, split_np

class Train_NN:
    def __init__(self, n_classes=2, hm_epochs=50, keep_rate=0.8, split_ratio=0.25):
        tf.reset_default_graph()
        self.n_classes = n_classes
        self.hm_epochs = hm_epochs
        self.keep_rate = keep_rate
        self.split_ratio = split_ratio
        
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
        
        self.cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.model, labels=self.y) )
        self.train_op = tf.train.AdamOptimizer().minimize(self.cost)
        self.saver = tf.train.Saver()
        
    def conv2d(self, tf_in, W, b):
        conv = tf.nn.conv2d(tf_in, W, strides=[1,1,1,1], padding='SAME')
        conv_with_b = tf.nn.bias_add(conv, b)
        conv_out = tf.nn.relu(conv_with_b)
        return conv_out
        
    def maxpool2d(self,tf_in):
        return tf.nn.max_pool(tf_in, ksize=[1,2,2,1], strides=[1,2,2,1],padding='SAME')
    
    def nn_load_data(self, verbose=False):
        x_np, y_np = load_labels()
        self.train_data_x, self.train_data_y, self.test_data_x, self.test_data_y = split_np(x_np, y_np, self.split_ratio)
        if (verbose):
            print("Traing_data count: ", len(self.train_data_x))
            print("Test_data count: ", len(self.test_data_x))
        
    def nn_model(self):
        x_tf = tf.reshape(self.x, shape=[-1,24,24,3])
        conv1 = self.maxpool2d(self.conv2d(x_tf, self.weights['W_conv1'], self.biases['b_conv1']))
        conv2 = self.maxpool2d(self.conv2d(conv1, self.weights['W_conv2'], self.biases['b_conv2']))
        fc = tf.reshape(conv2,[-1,6*6*64])
        fc = tf.nn.relu(tf.matmul(fc, self.weights['W_fc']) + self.biases['b_fc'])
        fc = tf.nn.dropout(fc, self.keep_rate)
        output = tf.matmul(fc, self.weights['W_out']) + self.biases['b_out']
        return output
    
    def nn_train(self, zero_catch=0, verbose=False):    
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            sess.run(tf.global_variables_initializer())
            loss_plot = []
            hm_zeros = 0
            for epoch in range(self.hm_epochs):
                c = 0
                _, c_tmp = sess.run([self.train_op, self.cost], feed_dict = {self.x: self.train_data_x, self.y: self.train_data_y})
                c += c_tmp
                loss_plot.append(c)
                if (verbose):
                    print('Epoch: ', epoch + 1, ' completed out of: ', self.hm_epochs, ' loss: ', c)
                if (zero_catch > 0) and (c == 0):
                    hm_zeros += 1
                    if hm_zeros == zero_catch:
                        if (verbose):
                            print("Reached zero catch of: ", zero_catch)
                        break
                elif (c != 0):
                    hm_zeros = 0
            plt.plot(loss_plot)
            plt.yscale('log')
            plt.show()
            location = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/tracking/saved_model/'
            save_path = self.saver.save(sess, location + "ball_model.ckpt")
            if (verbose):
                print("Model saved in path: %s" % save_path)

    def nn_test(self, verbose=True):
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            location = 'C:/Users/joear/OneDrive - Imperial College London/General/Code/Github/gait-lab/tracking/saved_model/'
            self.saver.restore(sess, location + "ball_model.ckpt")
            length = len(self.test_data_x)
            output = sess.run(self.nn_model(), feed_dict={self.x: self.test_data_x})
            output_result = output.argmax(axis=1)
            true_result = self.test_data_y.argmax(axis=1)
            accuracy = output_result + true_result
            ac = ((accuracy == 0) | (accuracy == 2))
            percent_acc = np.sum(ac)/len(ac)
            if (verbose):
                print(percent_acc)
            return percent_acc

#=======================================================================================================#

if __name__ == '__main__':
    print('-- Loading Data --')
    predictor = Train_NN(hm_epochs=200)
    predictor.nn_load_data(verbose=True)
    print('-- Training --')
    predictor.nn_train(zero_catch=2,verbose=True)
    print('-- Testing --')
    predictor.nn_test(verbose=True)



