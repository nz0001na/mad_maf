'''
This code is to generate train and test list for each single database
for FBC
'''
import os
import random


ro = '/home/na/1_MAD/1_code_supplement/bilinear_pooling/FactorizedBilinearCoding-master/data/mad-all/'
acc_ro = '/home/na/1_MAD/2_Data/1_compact_bp_data/Noiseprint/'

db_list = ['1_AMSL', '2_FERET_facemorpher', '3_FERET_opencv', '4_FERET_stylegan',
           '5_FRLL_facemorpher', '6_FRLL_opencv', '7_FRLL_stylegan', '8_FRLL_webmorph',
           '9_morph_facemorpher', '10_morph_opencv', '11_morph_stylegan']

folder_list = ['train/real', 'train/morph', 'test/morph', 'test/real']

for d in range(len(db_list)):
    # if d != 0: continue
    db = db_list[d]
    print(db)

    acc_path = acc_ro + db + '/'
    np_path = ro + db + '/noiseprint/'
    prnu_path = ro + db + '/prnu/'

    f_train = open('../data/mad-all/'+db+'/train_list.txt', 'w')
    f_test = open('../data/mad-all/'+db+'/test_list.txt', 'w')
    count1 = 0
    count2 = 0
    for fold in folder_list:
        # print(fold)
        set = fold.split('/')[0]
        label = fold.split('/')[1]
        img_list = os.listdir(acc_path + fold + '/')
        for img in img_list:
            img_name = img[0:len(img)-3] + 'jpg'
            if label == 'morph': lab = 0
            if label == 'real': lab = 1
            img1 = 'noiseprint/' + label + '/' + img_name
            img2 = 'prnu/' + label + '/' + img_name
            if os.path.exists(np_path +  label + '/' + img_name) is False: continue
            if os.path.exists(prnu_path + label + '/' + img_name) is False: continue
            if set == 'train':
                f_train.write(img1 + ' ' + img2 + ' ' + str(lab) + '\n')
                count1+=1
            if set == 'test':
                count2+=1
                f_test.write(img1 + ' ' + img2 + ' ' + str(lab) + '\n')
    print('train='+str(count1))
    print('test='+str(count2))
    f_train.close()
    f_test.close()