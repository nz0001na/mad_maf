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
import gc
import numpy as np

# # # load data from mat file

src_path = '../feature/mad_single/'
pos_neg_path = '../feature/mad_single_pos_neg/'
if os.path.exists(pos_neg_path) is False:
    os.makedirs(pos_neg_path)

db_list = ['1_AMSL', '2_FERET_facemorpher', '3_FERET_opencv', '4_FERET_stylegan',
           '5_FRLL_facemorpher', '6_FRLL_opencv', '7_FRLL_stylegan', '8_FRLL_webmorph',
            '9_morph_facemorpher', '10_morph_opencv', '11_morph_stylegan']

f = open('mad_single_result_linear.txt', 'w')

for db in db_list:
    # if db not in ['3_FERET_opencv']: continue        # '1_AMSL',
    print(db + '   *******************    ')
    train_data = sio.loadmat(src_path + db + '/train.mat')
    train_feature = train_data['feature']
    train_label = train_data['label'][0]
    test_data = sio.loadmat(src_path + db + '/test.mat')
    test_feature = test_data['feature']
    test_label = test_data['label'][0]

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
    f.write('  Accuracy = {:.4f}\n'.format(accuracy))

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

    sio.savemat(pos_neg_path + db + '_scores_linear.mat', {'positives': positives, 'negatives': negatives})

    EER = bob.measure.eer(negatives, positives, is_sorted=False, also_farfrr=False)
    print('  EER=' + str(EER))
    f.write('  EER = {:.4f}\n'.format(EER))

    npoints = 10000
    bob.measure.plot.det(negatives, positives, npoints, color='r', linestyle='-')
    bob.measure.plot.det_axis([0.01, 99.99, 0.01, 99.99])
    plt.xlabel('APCER (%)')
    plt.ylabel('BPCER (%)')
    plt.grid()
    plt.title(db)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.savefig(pos_neg_path + db + '_SVM_Linear.jpg')
    # plt.show()
    plt.close()
    gc.collect()
    # print('done')
f.close()



