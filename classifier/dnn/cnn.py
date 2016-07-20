import numpy as np
import tensorflow as tf
import math
import sys
import random
from osog.classifier.tool.file import *
import tensorflow.python.platform

NUM_CLASSES = 6
IMAGE_SIZE =32
IMAGE_PIXELS = IMAGE_SIZE*IMAGE_SIZE*3
layer1 = 32
layer2 = 128
layer3 = 512

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('train', 'train.txt', 'File name of train data')
flags.DEFINE_string('test', 'test.txt', 'File name of train data')
flags.DEFINE_string('train_dir', '/tmp/data', 'Directory to put the training data.')
flags.DEFINE_integer('max_steps', 10000, 'Number of steps to run trainer.')
flags.DEFINE_integer('batch_size', 10, 'Batch size'
                     'Must divide evenly into the dataset sizes.')
flags.DEFINE_float('learning_rate', 1e-6, 'Initial learning rate.')

def inference(images_placeholder, keep_prob):

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
        W_conv1 = weight_variable([5, 5, 3, layer1])
        b_conv1 = bias_variable([layer1])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

    with tf.name_scope('pool1') as scope:
        h_pool1 = max_pool_2x2(h_conv1)

    with tf.name_scope('conv2') as scope:
        W_conv2 = weight_variable([5, 5, layer1, layer2])
        b_conv2 = bias_variable([layer2])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    with tf.name_scope('pool2') as scope:
        h_pool2 = max_pool_2x2(h_conv2)

    with tf.name_scope('fc1') as scope:
        W_fc1 = weight_variable([math.floor(IMAGE_SIZE/4)*math.floor(IMAGE_SIZE/4)*layer2, layer3])
        b_fc1 = bias_variable([layer3])
        h_pool2_flat = tf.reshape(h_pool2, [-1, math.floor(IMAGE_SIZE/4)*math.floor(IMAGE_SIZE/4)*layer2])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    with tf.name_scope('fc2') as scope:
        W_fc2 = weight_variable([layer3, NUM_CLASSES])
        b_fc2 = bias_variable([NUM_CLASSES])

    with tf.name_scope('softmax') as scope:
        y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    return y_conv

def loss(logits, labels):
    cross_entropy = -tf.reduce_sum(labels*tf.log(logits))
    tf.scalar_summary("cross_entropy", cross_entropy)
    return cross_entropy

def training(loss, learning_rate):
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)
    return train_step

def accuracy(logits, labels):
    correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    tf.scalar_summary("accuracy", accuracy)
    return accuracy

class CNN:
    def __init__(self, dnn_name):
        self.images_placeholder = tf.placeholder("float", shape=(None, IMAGE_PIXELS))
        self.labels_placeholder = tf.placeholder("float", shape=(None, NUM_CLASSES))
        self.keep_prob = tf.placeholder("float")
        self.logits = inference(self.images_placeholder, self.keep_prob)
        self.sess = tf.InteractiveSession()
        self.saver = tf.train.Saver()
        self.sess.run(tf.initialize_all_variables())
        self.saver.restore(self.sess, os.path.join(os.path.dirname(__file__), 'learned/' + dnn_name + '.ckpt')
        )

    def predict(self, image):
        data = image.flatten().astype(np.float32) / 255.0
        image = np.asarray([data])
        return np.argmax(
            self.logits.eval(
                feed_dict={
                    self.images_placeholder: image,
                    self.keep_prob: 1.0
                }
            )[0]
        )

def create(name='unnamed', extensions=['png', 'jpg'], dataset_pathes=None):

    div_ratio = 0.9
    icz = read_dataset(dirpathes=dataset_pathes, exts=extensions, size=(IMAGE_SIZE,IMAGE_SIZE))
    random.shuffle(icz)
    train = icz[:math.floor(div_ratio * len(icz))]
    test = icz[math.floor(div_ratio * len(icz)):]
    train_images, train_classes = map(list, zip(*train))
    test_images, test_classes = map(list, zip(*test))

    train_image = []
    test_image = []
    for i in train_images:
        train_image.append(i.flatten().astype(np.float32) / 255.0)
    for i in test_images:
        test_image.append(i.flatten().astype(np.float32) / 255.0)

    train_label = []
    for c in train_classes:
        # ラベルを1-of-k方式で用意する
        tmp = np.zeros(len(dataset_pathes))
        tmp[int(c)] = 1
        train_label.append(tmp)
    train_image = np.asarray(train_image)
    train_label = np.asarray(train_label)

    test_label = []
    for c in test_classes:
        # ラベルを1-of-k方式で用意する
        tmp = np.zeros(len(dataset_pathes))
        tmp[int(c)] = 1
        test_label.append(tmp)
    test_image = np.asarray(test_image)
    test_label = np.asarray(test_label)

    with tf.Graph().as_default():
        # 画像を入れる仮のTensor
        images_placeholder = tf.placeholder("float", shape=(None, IMAGE_PIXELS))
        # ラベルを入れる仮のTensor
        labels_placeholder = tf.placeholder("float", shape=(None, NUM_CLASSES))
        # dropout率を入れる仮のTensor
        keep_prob = tf.placeholder("float")

        # inference()を呼び出してモデルを作る
        logits = inference(images_placeholder, keep_prob)
        # loss()を呼び出して損失を計算
        loss_value = loss(logits, labels_placeholder)
        # training()を呼び出して訓練
        train_op = training(loss_value, FLAGS.learning_rate)
        # 精度の計算
        acc = accuracy(logits, labels_placeholder)

        # 保存の準備
        saver = tf.train.Saver()
        # Sessionの作成
        sess = tf.Session()
        # 変数の初期化
        sess.run(tf.initialize_all_variables())
        # TensorBoardで表示する値の設定
        summary_op = tf.merge_all_summaries()
        summary_writer = tf.train.SummaryWriter(FLAGS.train_dir, sess.graph)

        # 訓練の実行
        for step in range(FLAGS.max_steps):
            lens = math.floor(len(train_image)/FLAGS.batch_size)
            for i in range(lens):
                # batch_size分の画像に対して訓練の実行
                sys.stdout.write("\r%d%%" % math.floor(i/lens*100))
                sys.stdout.flush()
                batch = FLAGS.batch_size*i
                # feed_dictでplaceholderに入れるデータを指定する
                sess.run(train_op, feed_dict={
                    images_placeholder:train_image[batch:batch+FLAGS.batch_size],
                    labels_placeholder:train_label[batch:batch+FLAGS.batch_size],
                    keep_prob:0.5})

            # 1 step終わるたびに精度を計算する
            train_accuracy = 0
            for i in range(lens):
                batch = FLAGS.batch_size * i
                train_accuracy += sess.run(acc, feed_dict={
                    images_placeholder: train_image[batch:batch+FLAGS.batch_size],
                    labels_placeholder: train_label[batch:batch+FLAGS.batch_size],
                    keep_prob: 1.0})
                if i == 0 and step%10 == 0:
                    summary_str = sess.run(summary_op, feed_dict={
                        images_placeholder: train_image[batch:batch+FLAGS.batch_size],
                        labels_placeholder: train_label[batch:batch+FLAGS.batch_size],
                        keep_prob: 1.0})
                    summary_writer.add_summary(summary_str, step)

            train_accuracy /= lens

            sys.stdout.write("\r")
            sys.stdout.flush()

            print("step %d, training accuracy %g"%(step, train_accuracy))

            #training accuracy = 1で終了させる
            if train_accuracy >= 0.998:
                break

            # 1 step終わるたびにTensorBoardに表示する値を追加する


    # 訓練が終了したらテストデータに対する精度を表示

    test_accuracy = 0
    lens = math.floor(len(test_image)/FLAGS.batch_size)
    for i in range(lens):
        batch = FLAGS.batch_size * i
        test_accuracy += sess.run(acc, feed_dict={
            images_placeholder: test_image[batch:batch+FLAGS.batch_size],
            labels_placeholder: test_label[batch:batch+FLAGS.batch_size],
            keep_prob: 1.0})
    if lens:
        test_accuracy /= lens
    print ("test accuracy %g"%test_accuracy)


    # 最終的なモデルを保存
    save_path = saver.save(sess,'learned/' +  name + '.ckpt')