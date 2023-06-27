import os
import random

ro = '/home/na/1_MAD/1_code_supplement/bilinear_pooling/FactorizedBilinearCoding-master/data/mad-fingerprinting/'
np_path = ro + 'noiseprint/'
prnu_path = ro + 'prnu/'

f_train = open('../data/mad-fingerprinting/train_list.txt', 'w')
f_test = open('../data/mad-fingerprinting/test_list.txt', 'w')
c1, c2 = 0,0
cat_list = os.listdir(np_path)
for cat in cat_list:
    print(cat)
    label = cat

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
            if os.path.exists(np_path + cat + '/' + db + '/' + img_name) is False:
                print('np')
                continue
            if os.path.exists(prnu_path + cat + '/' + db + '/' + img_name) is False:
                print('prnu')
                continue
            f_train.write(img1 + ' ' + img2 + ' ' + str(label) + '\n')
            c1 += 1

        for i in range(split, count):
            img_name = img_list[i]
            img1 = 'noiseprint/' + cat + '/' + db + '/' + img_name
            img2 = 'prnu/' + cat + '/' + db + '/' + img_name
            if os.path.exists(np_path + cat + '/' + db + '/' + img_name) is False:
                print('np')
                continue
            if os.path.exists(prnu_path + cat + '/' + db + '/' + img_name) is False:
                print('prnu')
                continue
            f_test.write(img1 + ' ' + img2 + ' ' + str(label) + '\n')
            c2 += 1
print('c1=' +str(c1))
print('c2='+str(c2))
f_train.close()
f_test.close()