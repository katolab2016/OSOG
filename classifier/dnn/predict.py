import sys
import numpy as np
import tensorflow as tf
import cv2
from osog.classifier.tool import file

NUM_CLASSES = 4
IMAGE_SIZE = 32
IMAGE_PIXELS = IMAGE_SIZE*IMAGE_SIZE*3

def inference(images_placeholder, keep_prob):
    """ モデルを作成する関数
    引数:
      images_placeholder: inputs()で作成した画像のplaceholder
      keep_prob: dropout率のplace_holder

    返り値:
      cross_entropy: モデルの計算結果
    """
    def weight_variable(shape):
      initial = tf.truncated_normal(shape, stddev=0.1)
      return tf.Variable(initial)

    def bias_variable(shape):
      initial = tf.constant(0.1, shape=shape)
      return tf.Variable(initial)

    def conv2d(x, W):
      return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2x2(x):
      return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                            strides=[1, 2, 2, 1], padding='SAME')

    x_image = tf.reshape(images_placeholder, [-1, IMAGE_SIZE, IMAGE_SIZE, 3])

    with tf.name_scope('conv1') as scope:
        W_conv1 = weight_variable([5, 5, 3, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    with tf.name_scope('pool1') as scope:
        h_pool1 = max_pool_2x2(h_conv1)

    with tf.name_scope('conv2') as scope:
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    with tf.name_scope('pool2') as scope:
        h_pool2 = max_pool_2x2(h_conv2)

    with tf.name_scope('fc1') as scope:
        W_fc1 = weight_variable([8*8*64, 1024])
        b_fc1 = bias_variable([1024])
        h_pool2_flat = tf.reshape(h_pool2, [-1, 8*8*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    with tf.name_scope('fc2') as scope:
        W_fc2 = weight_variable([1024, NUM_CLASSES])
        b_fc2 = bias_variable([NUM_CLASSES])

    with tf.name_scope('softmax') as scope:
        y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    return y_conv

class DNN:
    def __init__(self, dnn_name):
        self.images_placeholder = tf.placeholder("float", shape=(None, IMAGE_PIXELS))
        self.labels_placeholder = tf.placeholder("float", shape=(None, NUM_CLASSES))
        self.keep_prob = tf.placeholder("float")
        self.logits = inference(self.images_placeholder, self.keep_prob)
        self.sess = tf.InteractiveSession()
        self.saver = tf.train.Saver()
        self.sess.run(tf.initialize_all_variables)
        self.saver.restore(self.sess, dnn_name + '.ckpt')

    #def predict(self, image):


if __name__ == '__main__':
    test_image = []
    ims = file.imsread_ext('datasets/beetle/', exts=['jpg','png'],size=(IMAGE_SIZE, IMAGE_SIZE))
    for i in ims:
        test_image.append(i.flatten().astype(np.float32)/255.0)
    test_image = np.asarray(test_image)

    images_placeholder = tf.placeholder("float", shape=(None, IMAGE_PIXELS))
    labels_placeholder = tf.placeholder("float", shape=(None, NUM_CLASSES))
    keep_prob = tf.placeholder("float")

    logits = inference(images_placeholder, keep_prob)
    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    sess.run(tf.initialize_all_variables())
    saver.restore(sess, "model.ckpt")

    for i in range(len(test_image)):
        pred = np.argmax(logits.eval(feed_dict={
            images_placeholder: [test_image[i]],
            keep_prob: 1.0 })[0])
        print(pred)