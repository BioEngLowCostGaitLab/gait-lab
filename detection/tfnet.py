import tensorflow as tf
import numpy as np
import argparse
import os
from os.path import join

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=join('/home', 'antti', 'Projects', 'gait-lab'), type=str) # path to images
    parser.add_argument('--imgdir', default=join('/home', 'antti', 'Projects', 'gait-lab', 'detection', 'resources'), type=str) # path to save figures
    parser.add_argument('--modeldir', default=join('/home', 'antti', 'Projects', 'gait-lab', 'detection', 'tfmodels'), type=str) # path to save models
    parser.add_argument('--batchSize', default=64, type=int)
    parser.add_argument('--maxEpochs', default=20, type=int) # epochs to train for
    parser.add_argument('--trainedEpochs', default=0, type=int) # previously trained epochs on same parameters
    parser.add_argument('--lr', default=1e-4, type=float) # learning rate
    parser.add_argument('--fSize', default=64, type=int)  # multiple of filters to use

    return parser.parse_args()

def create_dataset(opts, datafile):
    imgdir = opts.imgdir
    f = open(join(imgdir, datafile), 'r')
    file = f.readlines()
    imgs, labels = [], []

    for line in file:
        imgs.append(join(imgdir, 'images', 'train', line.split(',')[0]))
        labels.append((int(line.split(',')[1])))

    imgs = tf.constant(imgs)
    labels = tf.constant(labels)
    return imgs, labels

def _parse_function(filename, label):
    image_string = tf.read_file(filename)
    image_decoded = tf.image.decode_image(image_string)
    return image_decoded, label

opts = get_args()

#sess = tf.Session()
filenames, labels = create_dataset(opts, 'trainlabels.txt')
dataset = tf.contrib.data.Dataset.from_tensor_slices((filenames, labels))
dataset = dataset.map(_parse_function)
batched_dataset = dataset.batch(4)
iterator = batched_dataset.make_one_shot_iterator()


x = tf.placeholder(tf.float32, [3072, 1])
W = tf.Variable(tf.zeros([3072, 1]))
b = tf.Variable(tf.zeros([1]))
y = tf.matmul(tf.transpose(W), x) + b

y_ = tf.placeholder(tf.float32, [1])

cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

for _ in range(5):
    batch_xs, batch_ys = iterator.get_next()
    batch_xs = tf.reshape(batch_xs, [3072, 1])
    sess.run(train_step, feed_dict={x: batch_xs.eval(), y_: batch_ys.eval()})


correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver()
save_path = saver.save(sess, join(os.getcwd(), 'model.ckpt'))
print("Model saved in file: %s" % save_path)
