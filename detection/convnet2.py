import tensorflow as tf
import argparse
import os
from os.path import join
from tensorflow.python.tools.freeze_graph import freeze_graph
from tffunctions import _parse_function, augment, Net


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgdir', default=join(os.getcwd(), 'resources'), type=str) # path to save figures
    parser.add_argument('--batchSize', default=32, type=int)
    parser.add_argument('--maxEpochs', default=40, type=int) # epochs to train for
    parser.add_argument('--lr', default=1e-4, type=float) # learning rate

    return parser.parse_args()


def create_dataset(opts, datafile, train=True):
    imgdir = opts.imgdir
    f = open(join(imgdir, datafile), 'r')
    file = f.readlines()
    imgs, labels = [], []

    for line in file:
        if '_0.' in line or '_1.' in line or '_2.' in line or '_3.' in line: #yeah...
            if train:
                path = join(imgdir, 'images', 'saved_images', line.split(',')[0])
            else:
                path = join(imgdir, 'images', 'saved_images', line.split(',')[0])
            imgs.append(path)
            labels.append((int(line.split(',')[1])))

    dataset_length = len(labels)
    imgs = tf.constant(imgs)
    labels = tf.constant(labels)
    return imgs, labels, dataset_length

opts = get_args()

# Training Parameters
batch_size = opts.batchSize
n_epochs = opts.maxEpochs * 2 # fix this bug

opts = get_args()

images, labels, dataset_length = create_dataset(opts, 'labels_new.txt')
print(labels.eval(session = tf.Session()))

dataset = tf.contrib.data.Dataset.from_tensor_slices((images, labels))
dataset = dataset.map(_parse_function)
dataset = dataset.repeat(n_epochs)
dataset = dataset.batch(batch_size)
iterator = dataset.make_one_shot_iterator()
n_batches = dataset_length // batch_size

test_images, test_labels, test_length = create_dataset(opts, 'testlabels.txt', train=False)
testset = tf.contrib.data.Dataset.from_tensor_slices((test_images, test_labels))
testset = testset.map(_parse_function)
testset = testset.repeat(n_epochs)
testset = testset.batch(test_length)
test_iterator = testset.make_one_shot_iterator()



# tf Graph input
x = tf.placeholder("float", [None, 24, 24, 3])
y = tf.placeholder("float", [None, 1])


# Construct model
pred = Net(x)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=opts.lr).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph

with tf.Session() as sess:
    sess.run(init)
    # Training cycle
    for epoch in range(n_epochs // 2): # for some reason bugs with outofrange with all epochs
        # Loop over all batches
        avg_cost = 0.0
        for i in range(n_batches):
            batch_x, batch_y = iterator.get_next()
            batch_y = tf.reshape(batch_y, [batch_size, 1])
            batch_x = tf.squeeze(augment(batch_x, 32), [1])
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x.eval(),
                                                          y: batch_y.eval()})
            #predict_marker = tf.greater(tf.squeeze(tf.squeeze(pred, [-1]), [-1]), 0.5)
            #correct_prediction = tf.equal(tf.to_float(predict_marker), y)
        # Calculate accuracy
            #accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            #X_test, Y_test = test_iterator.get_next()
            #Y_test = tf.reshape(Y_test, [test_length, 1])
            #print("Accuracy:", accuracy.eval({x: batch_x.eval(), y: batch_y.eval()}))
            # Compute average loss
            avg_cost += c / batch_size
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))

    # Test model
        #predict_marker = tf.greater(tf.squeeze(tf.squeeze(pred, [-1]), [-1]), 0.5)
        #correct_prediction = tf.equal(tf.to_float(predict_marker), y)
    # Calculate accuracy
        #accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        #X_test, Y_test = test_iterator.get_next()
        #Y_test = tf.reshape(Y_test, [test_length, 1])
        #print("Accuracy:", accuracy.eval({x: X_test.eval(), y: Y_test.eval()}))


    saver = tf.train.Saver()
    save_path = saver.save(sess, join(os.getcwd(), 'edp_model.ckpt'))
    print("Model saved in file: %s" % save_path)
