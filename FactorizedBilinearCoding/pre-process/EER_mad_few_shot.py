import os
import matplotlib.pyplot as plt
import scipy.io as sio
import bob.measure
import gc


dst_path = '../feature/mad_few_shot_pos_neg/'

for file in os.listdir(dst_path):
    if file.split('.')[1] != 'mat': continue
    print(file)
    data = sio.loadmat(dst_path + file)
    positives = data['positives'].flatten()
    negatives = data['negatives'].flatten()

    # EER
    EER = bob.measure.eer(negatives, positives, is_sorted=False, also_farfrr=False)
    print('*****************  EER=' + str(EER))

    # DET
    npoints = 10000
    bob.measure.plot.det(negatives, positives, npoints, color='r', linestyle='-')
    bob.measure.plot.det_axis([0.01, 99.99, 0.01, 99.99])
    plt.xlabel('APCER (%)')
    plt.ylabel('BPCER (%)')
    plt.grid()
    plt.title(file)
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    plt.savefig(dst_path + file+ '.jpg')
    # plt.show()
    plt.close()
    gc.collect()
    # print('done')

    #  APCER reports the proportion of morph attack samples incorrectly classified as
    #  bona fide presentation. This is measured as the (M)number of incorrectly
    #  classified morphed images, divided by the total number of morphed images (N_m)

    # BPCER is the proportion of bona fide samples incorrectly classified as morphed samples.
    # This is measured as the number of incorrectly classified bona fide images (B),
    # divided by the total number of bona fide images (N_b)
    M_data = negatives #.flatten()
    B_data = positives #.flatten()
    N_m = len(M_data)
    N_b = len(B_data)
    M = 0
    B = 0
    for mm in range(len(M_data)):
        value = M_data[mm]
        if value >= 0.5: M += 1
    for bb in range(len(B_data)):
        value = B_data[bb]
        if value < 0.5: B += 1
    acc = ((N_m - M) + (N_b - B)) / (N_m + N_b) * 1.0
    BPCER = B / (N_b * 1.0)
    APCER = M / (N_m * 1.0)
    ACER = (APCER + BPCER) / 2.0
    print('*****************  ACC=' + str(acc))
    print('*****************  BPCER=' + str(BPCER))
    print('*****************  APCER=' + str(APCER))
    print('*****************  ACER=' + str(ACER))