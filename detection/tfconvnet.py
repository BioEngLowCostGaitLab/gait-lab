import tensorflow as tf
import argparse
from os.path import join
import os
from tensorflow.python.tools.freeze_graph import freeze_graph


# ok, currently not a convolutional net. the point is to make it one though once everything else is running properly
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgdir', default=join(os.getcwd(), 'resources'), type=str) # path to save figures
    parser.add_argument('--batchSize', default=32, type=int)
    parser.add_argument('--maxEpochs', default=100, type=int) # epochs to train for
    parser.add_argument('--trainedEpochs', default=0, type=int) # previously trained epochs on same parameters
    parser.add_argument('--lr', default=1e-4, type=float) # learning rate
    parser.add_argument('--fSize', default=64, type=int)  # multiple of filters to use

    return parser.parse_args()


def create_dataset(opts, datafile, train=True):
    imgdir = opts.imgdir
    f = open(join(imgdir, datafile), 'r')
    file = f.readlines()
    imgs, labels = [], []

    for line in file:
        if train:
            path = join(imgdir, 'images', 'train', line.split(',')[0])
        else:
            path = join(imgdir, 'images', 'test', line.split(',')[0])
        imgs.append(path)
        labels.append((int(line.split(',')[1])))

    dataset_length = len(labels)
    imgs = tf.constant(imgs)
    labels = tf.constant(labels)
    return imgs, labels, dataset_length

def _parse_function(filename, label):
    image_string = tf.read_file(filename)
    image_decoded = tf.image.decode_image(image_string)
    return image_decoded, label

def multilayer_perceptron(x, weights, biases):

    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

opts = get_args()

# Training Parameters
batch_size = opts.batchSize
n_epochs = opts.maxEpochs * 2 # fix this bug

# Network Parameters
num_input = 3072
num_classes = 1
dropout = 0.1 # Dropout, probability to drop a unit

opts = get_args()

images, labels, dataset_length = create_dataset(opts, 'trainlabels.txt')

dataset = tf.contrib.data.Dataset.from_tensor_slices((images, labels))
dataset = dataset.map(_parse_function)
dataset = dataset.repeat(n_epochs)
dataset = dataset.batch(batch_size)
iterator = dataset.make_one_shot_iterator()
n_batches = dataset_length // batch_size

test_images, test_labels, test_length = create_dataset(opts, 'testlabels.txt', train=False)
print(test_length)
testset = tf.contrib.data.Dataset.from_tensor_slices((test_images, test_labels))
testset = testset.map(_parse_function)
testset = testset.repeat(n_epochs)
testset = testset.batch(test_length)
test_iterator = testset.make_one_shot_iterator()
display_step = 1


# Network Parameters
n_hidden_1 = 1500 # 1st layer number of features
n_hidden_2 = 1500 # 2nd layer number of features
n_input = 3072 # Number of features


# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, 1])


# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, 1]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([1]))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

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
            batch_x = tf.reshape(batch_x, [batch_size, 3072])
            batch_y = tf.reshape(batch_y, [batch_size, 1])
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x.eval(),
                                                          y: batch_y.eval()})
            # Compute average loss
            avg_cost += c / batch_size
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))

    # Test model
        predict_marker = tf.greater(pred, 0.5)
        correct_prediction = tf.equal(tf.to_float(predict_marker), y)
    # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        X_test, Y_test = test_iterator.get_next()
        X_test = tf.reshape(X_test, [test_length, 3072])
        Y_test = tf.reshape(Y_test, [test_length, 1])
        print("Accuracy:", accuracy.eval({x: X_test.eval(), y: Y_test.eval()}))


    saver = tf.train.Saver()
    save_path = saver.save(sess, join(os.getcwd(), 'edp_model.ckpt'))
    print("Model saved in file: %s" % save_path)
