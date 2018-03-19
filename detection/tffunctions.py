import tensorflow as tf

def _parse_function(filename, label):
    image_string = tf.read_file(filename)
    image_decoded = tf.image.decode_image(image_string)
    sess = tf.Session()
    return image_decoded, label

def augment(images, batch_size):
    transformed_images = []
    for i in range(batch_size):
        transformed_images.append(
        tf.expand_dims(
                       tf.image.random_flip_up_down(
                       tf.image.random_flip_left_right(images[i, :, :, :]), 0), 0))
    out = tf.convert_to_tensor(transformed_images)
    #out = tf.image.resize_images(out, [24, 24])
    return out


def Net(x):
    fSize = 32
    # Hidden layer with RELU activation
    x = tf.layers.conv2d(x, fSize, 5, strides=(2,2),
    activation=tf.nn.relu)
    x = tf.layers.conv2d(x, 2 * fSize, 5, strides=(2,2),
    activation=tf.nn.relu)
    x = tf.reshape(x, [-1, 576])
    #x = tf.layers.dense(x, 30, activation=tf.nn.relu)
    x = tf.layers.dense(x, 1)
    x = tf.nn.sigmoid(x)
    return x
