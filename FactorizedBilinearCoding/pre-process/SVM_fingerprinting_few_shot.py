'''
this code is to use SVM to do multi-class fingerprinting
feature is extracted by FBC
and compute EER
plot DET
'''

import os
from sklearn.svm import SVC
import scipy.io as sio
import gc
import numpy as np
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.metrics import fbeta_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# # # load data from mat file

src_path = '../feature/mad-fingerprinting/'
pos_neg_path = '../feature/mad-fingerprinting_pos_neg/'
if os.path.exists(pos_neg_path) is False:
    os.makedirs(pos_neg_path)

train_list = [['1_FRLL_1_shot_train.mat', '1_FRLL_5_shot_train.mat'],
            ['2_FERET_1_shot_train.mat', '2_FERET_5_shot_train.mat'],
            ['3_FRGC_1_shot_train.mat', '3_FRGC_5_shot_train.mat'],
            ['4_CelebA_1_shot_train.mat', '4_CelebA_5_shot_train.mat'],
            ['5_self_1_shot_train.mat', '5_self_5_shot_train.mat'],
            ['6_all_1_shot_train.mat', '6_all_5_shot_train.mat']]
test_list = [ '1_FRLL_test.mat',
             '2_FERET_test.mat',
             '3_FRGC_test.mat',
             '4_CelebA_test.mat',
             '5_self_test.mat',
             '6_all_test.mat']
f = open('fingerprinting_result_linear.txt', 'w')

for i in range(len(train_list)):
    test_file = src_path + test_list[i]
    print(test_file[i])
    test_data = sio.loadmat(test_file)
    test_feature = test_data['feature']
    test_label = test_data['label'].flatten() + 1
    for shot in range(2):
        train_file = src_path + train_list[i][shot]
        print(train_list[i][shot])
        name = train_list[i][shot]
        train_data = sio.loadmat(train_file)
        train_feature = train_data['feature']
        train_label = train_data['label'].flatten() + 1

        print(np.shape(train_feature))
        print(np.shape(train_label))
        print(np.shape(test_feature))
        print(np.shape(test_label))

        clf = SVC(kernel='linear', probability=True)
        clf.fit(train_feature, train_label)
        accuracy = clf.score(test_feature, test_label)
        print('******* Accuracy: {}'.format(accuracy))
        test_pred = clf.predict(test_feature)

        f1 = f1_score(test_label, test_pred, average='macro')
        print('******* f1: {}'.format(f1))
        f_beta = fbeta_score(test_label, test_pred, average='macro', beta=0.5)
        print('******* f_beta: {}'.format(f_beta))
        y_pred = clf.predict_proba(test_feature)
        roc = roc_auc_score(test_label, y_pred, multi_class='ovr')
        print('******* roc: {}'.format(roc))

        # non normalized
        mt = confusion_matrix(test_label, test_pred, labels=clf.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=mt, display_labels=clf.classes_)
        disp.plot()
        plt.show()
        plt.savefig(pos_neg_path + name + '_1.jpg')
        plt.close()
        print(mt)

        # normalized
        mt2 = confusion_matrix(test_label, test_pred, normalize='all')
        disp = ConfusionMatrixDisplay(confusion_matrix=mt2, display_labels=clf.classes_)
        disp.plot()
        plt.show()
        plt.savefig(pos_neg_path + name + '_2.jpg')
        plt.close()
        print(mt2)

        # dict = {}
        # dict['train_feature'] = train_feature
        # dict['train_label'] = train_label
        # # d = {}
        # dict['test_feature'] = test_feature
        # dict['test_label'] = test_label
        # sio.savemat(pos_neg_path + name + '_pos_neg.mat', dict)
f.close()



