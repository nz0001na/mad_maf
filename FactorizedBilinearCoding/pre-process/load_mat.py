'''
this code is to use SVM to do multi-class fingerprinting
feature is extracted by FBC
and compute EER
plot DET
'''

import os
# from sklearn.svm import SVC
# import matplotlib.pyplot as plt
import scipy.io as sio
# import bob.measure
# import gc
import numpy as np

# # # load data from mat file

src_path = '../feature/mad-fingerprinting/'
pos_neg_path = '../feature/mad-fingerprinting_pos_neg/'
if os.path.exists(pos_neg_path) is False:
    os.makedirs(pos_neg_path)

train_list = [
            # '1_FRLL_1_shot_train.mat', '1_FRLL_5_shot_train.mat',
            '2_FERET_1_shot_train.mat', '2_FERET_5_shot_train.mat',
            '3_FRGC_1_shot_train.mat', '3_FRGC_5_shot_train.mat',
            '4_CelebA_1_shot_train.mat', '4_CelebA_5_shot_train.mat',
            '5_self_1_shot_train.mat', '5_self_5_shot_train.mat',
            '6_all_1_shot_train.mat', '6_all_1_shot_train.mat']
test_list = [ '1_FRLL_test.mat',
             '2_FERET_test.mat',
             '3_FRGC_test.mat',
             '4_CelebA_test.mat',
             '5_self_test.mat',
             '6_all_test.mat']

for mo in train_list:
    print(mo)
    test_data = sio.loadmat(src_path + mo)
    test_feature = test_data['feature']
    test_label = test_data['label'].flatten() + 1

    print(np.shape(test_feature))
    print(np.shape(test_label))
    print('d')




