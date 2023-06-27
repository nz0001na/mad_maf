'''
this code is to use SVM to classify bona fide (1) and morphed (0) face images
feature is extracted by texture feature based methods
and compute EER
plot DET
'''

import os
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import scipy.io as sio
import bob.measure
import numpy as np

# # # load data from mat file

src_path = '../feature/mad-fingerprinting/'
models = os.listdir(src_path)
for model in models:
    print(model)
    src_file = src_path + model
    da = sio.loadmat(src_file)
    fea = da['feature']
    label = da['label'].flatten()
    cunt = len(fea)
    train_feature = []
    train_label = []
    test_feature = []
    test_label = []
    for i in range(cunt):
        f = fea[i]
        l = label[i]
        if i%5 == 0:
            test_feature.append(f)
            test_label.append(l)
        else:
            train_feature.append(f)
            train_label.append(l)


    train_feature = np.asarray(train_feature)
    train_label = np.asarray(train_label)
    test_feature = np.asarray(test_feature)
    test_label = np.asarray(test_label)
    print(np.shape(train_feature))
    print(np.shape(train_label))
    print(np.shape(test_feature))
    print(np.shape(test_label))

    # train model
    # print(' SVM-Linear begin training: ')
    clf = SVC(kernel='linear', probability=True)
    clf.fit(train_feature, train_label)
    accuracy = clf.score(test_feature, test_label)
    print('  Accuracy: {}'.format(accuracy))

    # # predict and generate positives and negatives
    positives = []
    negatives = []
    y_pred = clf.predict_proba(test_feature)
    test_pred = y_pred[:,1]
    for i in range(len(test_pred)):
        if test_label[i] == 1:
            positives.append(test_pred[i])
        else:
            negatives.append(test_pred[i])

    EER = bob.measure.eer(negatives, positives, is_sorted=False, also_farfrr=False)
    print('  EER=' + str(EER))






