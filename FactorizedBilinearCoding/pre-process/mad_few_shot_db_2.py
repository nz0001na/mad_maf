import os


ro = '/home/na/1_MAD/1_code_supplement/bilinear_pooling/FactorizedBilinearCoding-master/data/mad-all/few_shot_mad/'
np_path = ro + 'noiseprint/'
prnu_path = ro + 'prnu/'

sets = ['A_set', 'B_set', 'C_set']
shots = ['1_shot', '5_shot']
folder_list = ['train/real', 'train/fake', 'test/fake', 'test/real']

for set in sets:
    print(set)
    for shot in shots:
        print(shot)
        np_path1 = np_path + set + '/' + shot + '/'
        prnu_path2 = prnu_path + set +'/' + shot + '/'

        f_train = open(ro + set + '_' + shot + '_train_list.txt', 'w')
        f_test = open(ro + set + '_' + shot + '_test_list.txt', 'w')
        count1 = 0
        count2 = 0
        for fold in folder_list:
            se = fold.split('/')[0]
            label = fold.split('/')[1]
            img_list = os.listdir(np_path1 + fold + '/')
            for img in img_list:
                img_name1 = img
                img_name2 = img[0:len(img) - 3] + 'jpg'
                if label == 'fake': lab = 0
                if label == 'real': lab = 1
                img1 = 'noiseprint/' + set +'/' + shot + '/' + fold + '/' + img_name1
                img2 = 'prnu/' + set +'/' + shot + '/' + fold + '/' + img_name2
                if os.path.exists(np_path1 + fold + '/' + img_name1) is False:
                    print('np')
                    continue
                if os.path.exists(prnu_path2 + fold + '/' + img_name2) is False:
                    print('prnu')
                    continue
                if se == 'train':
                    f_train.write(img1 + ' ' + img2 + ' ' + str(lab) + '\n')
                    count1 += 1
                if se == 'test':
                    count2 += 1
                    f_test.write(img1 + ' ' + img2 + ' ' + str(lab) + '\n')
        print('train=' + str(count1))
        print('test=' + str(count2))
        f_train.close()
        f_test.close()



