import numpy as np
import tensorflow as tf
import os.path
from noiseprint.network import FullConvNet
from noiseprint.utility.utilityRead import imread2f


ro = '/media/zn/BE2C40612C4016B5/2_zn_research/1_MAD/Code/3_quality_feature_extraction/'

tf.reset_default_graph()
x_data  = tf.placeholder(tf.float32, [1, None, None, 1], name="x_data")
net = FullConvNet(x_data, 0.9, tf.constant(False),  num_levels=17)
saver = tf.train.Saver(net.variables_list)

configSess = tf.ConfigProto(); configSess.gpu_options.allow_growth = True
chkpt_fname = ro + '3_noiseprint_extraction/noiseprint/nets/net_jpg101/model'

with tf.Session(config=configSess) as sess:
    saver.restore(sess, chkpt_fname)

a = net.variables_list
b = net.output
c = net.level
d = net.input
e = net.trainable_list






imgfilename = 'example/morph3.jpg'
img, mode = imread2f(imgfilename, channel=1)
QF = 200
print(' %dx%d small %3d' % (img.shape[0], img.shape[1], QF))
res = sess.run(net.output, feed_dict={x_data: img[np.newaxis,:,:,np.newaxis]})
res = np.squeeze(res)

# net.summary
print('f')