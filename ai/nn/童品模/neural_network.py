#!/usr/bin/python2.7
#coding:utf-8

'''
A logistic regression learning algorithm example using TensorFlow library.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)
Author:
'''

from __future__ import print_function

import tensorflow as tf
import random

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("../Mnist_data/", one_hot=True)
print(mnist)

tf.set_random_seed(777)

# Parameters setting
learning_rate = 0.0001
training_epochs = 250 # 训练迭代的次数
batch_size = 100   # 一次输入的样本
display_step=1

# set the tf Graph Input & set the model weights
# 92.8%
x=tf.placeholder(dtype=tf.float32,shape=[None,784],name='input_x')
y=tf.placeholder(dtype=tf.float32,shape=[None,10],name='input_y')

#set layers
W1=tf.Variable(tf.random_normal([784,200]))
b1=tf.Variable(tf.random_normal([200]))
L1=tf.nn.relu(tf.matmul(x,W1)+b1)

W2=tf.Variable(tf.random_normal([200,50]))
b2=tf.Variable(tf.random_normal([50]))
L2=tf.nn.relu(tf.matmul(L1,W2)+b2)

W3=tf.Variable(tf.random_normal([50,10]))
b3=tf.Variable(tf.random_normal([10]))
L3=tf.matmul(L2,W3)+b3 #
pred=tf.nn.softmax(L3)

# Construct the model
# TO DO

print(pred.shape)
# Minimize error using cross entropy & set the gradient descent
# tf.nn.softmax_cross_entropy_with_logits(logits=L3,labels=y)求出来的是一个vector,n_sample*10,求平均变成一个数；
cost=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=L3,labels=y))
# cost=tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred),reduction_indices=1)) #交叉熵，reducion_indices=1横向求和
optimizer=tf.train.AdamOptimizer(learning_rate).minimize(cost)


# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

# Start training
with tf.Session() as sess:

    # Run the initializer
    #
    sess.run(init)

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs,
                                                          y: batch_ys})
            # Compute average loss
            avg_cost += c / total_batch
        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))

    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print("Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))