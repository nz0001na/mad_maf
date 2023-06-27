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

src_path = '../feature/mad_few_shot/'
dst_path = '../feature/mad_few_shot_fig/'
if os.path.exists(dst_path) is False:
    os.makedirs(dst_path)

sets = ['A_set', 'B_set', 'C_set']
shots = ['1_shot', '5_shot']

for set in sets:
    for shot in shots:
        tag = set + '_' + shot
        print(tag)
        dst_train_fake = dst_path + set + '/' + shot + '/train/fake/'
        dst_train_real = dst_path + set + '/' + shot + '/train/real/'
        dst_test_fake = dst_path + set + '/' + shot + '/test/fake/'
        dst_test_real = dst_path + set + '/' + shot + '/test/real/'
        if os.path.exists(dst_train_fake) is False: os.makedirs(dst_train_fake)
        if os.path.exists(dst_train_real) is False: os.makedirs(dst_train_real)
        if os.path.exists(dst_test_fake) is False: os.makedirs(dst_test_fake)
        if os.path.exists(dst_test_real) is False: os.makedirs(dst_test_real)
        n, m = 0, 0
        train_data = sio.loadmat(src_path + tag + '_train.mat')
        train_feature = train_data['feature']
        train_label = train_data['label'][0]
        print(len(train_label))
        for i in range(len(train_feature)):
            fi = train_feature[i]
            fea = fi.reshape((64,64))
            fea *= 255.0 / fea.max()
            label = train_label[i]
            if label == 0:
                name = 'fake_' + str(n) + '.jpg'
                cv2.imwrite(dst_train_fake + name, fea)
            if label == 1:
                name = 'real_' + str(n) + '.jpg'
                cv2.imwrite(dst_train_real + name, fea)
            n +=1

        test_data = sio.loadmat(src_path + tag + '_test.mat')
        test_feature = test_data['feature']
        test_label = test_data['label'][0]
        print(test_label)
        for j in range(len(test_feature)):
            fi = test_feature[j]
            fea = fi.reshape((64,64))
            fea *= 255.0 / fea.max()
            label = test_label[j]
            if label == 0:
                name = 'fake_' + str(m) + '.jpg'
                cv2.imwrite(dst_test_fake + name, fea)
            if label == 1:
                name = 'real_' + str(m) + '.jpg'
                cv2.imwrite(dst_test_real + name, fea)
            m +=1

