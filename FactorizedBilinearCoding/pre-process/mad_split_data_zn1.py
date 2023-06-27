import os
import random

ro = '/home/na/1_MAD/1_code_supplement/bilinear_pooling/FactorizedBilinearCoding-master/data/mad-all/'
np_path = ro + 'noiseprint/'
prnu_path = ro + 'prnu/'

f_train = open('../data/mad-all/train_list.txt', 'w')
f_test = open('../data/mad-all/test_list.txt', 'w')

cat_list = os.listdir(np_path)
for cat in cat_list:
    print(cat)
    if cat == 'fake': label = 0
    if cat == 'real': label = 1

    db_list = os.listdir(np_path + cat)
    for db in db_list:
        print(db)
        img_list = os.listdir(np_path + cat + '/' + db)
        count = len(img_list)
        split = int(0.8*count)
        random.shuffle(img_list)
        for i in range(0, split):
            img_name = img_list[i]
            img1 = 'noiseprint/' + cat + '/' + db + '/' + img_name
            img2 = 'prnu/' + cat + '/' + db + '/' + img_name
            f_train.write(img1 + ' ' + img2 + ' ' + str(label) + '\n')

        for i in range(split, count):
            img_name = img_list[i]
            img1 = 'noiseprint/' + cat + '/' + db + '/' + img_name
            img2 = 'prnu/' + cat + '/' + db + '/' + img_name
            f_test.write(img1 + ' ' + img2 + ' ' + str(label) + '\n')

f_train.close()
f_test.close()