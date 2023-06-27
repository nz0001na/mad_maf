'''
this code is to use SVM to classify bona fide (1) and morphed (0) face images
feature is extracted by texture feature based methods
and compute EER
plot DET
'''

import os
import scipy.io as sio
import cv2

# # # load data from mat file

src_path = '../feature/mad-fingerprinting/'
dst_path = '../feature/mad-fingerprinting_fig/'
if os.path.exists(dst_path) is False:
    os.makedirs(dst_path)

files = os.listdir(src_path)
for file in files:
    print(file)
    name = file.split('.')[0]
    n = 0
    train_data = sio.loadmat(src_path + file)
    train_feature = train_data['feature']
    train_label = train_data['label'].flatten() + 1
    print(len(train_label))
    if os.path.exists(dst_path + name) is False: os.makedirs(dst_path + name)
    for i in range(len(train_feature)):
        fi = train_feature[i]
        fea = fi.reshape((64,64))
        fea *= 255.0 / fea.max()
        label = train_label[i]
        if os.path.exists(dst_path + name + '/' + str(label)) is False:
            os.makedirs(dst_path + name + '/' + str(label))
        fig_name = str(label) + '_' + str(n) + '.jpg'
        cv2.imwrite(dst_path + name + '/' + str(label) + '/' + fig_name, fea)
        n += 1
