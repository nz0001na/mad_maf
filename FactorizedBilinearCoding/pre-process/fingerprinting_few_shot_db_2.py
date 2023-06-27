import os
import shutil


ro = '/home/na/1_MAD/1_code_supplement/bilinear_pooling/FactorizedBilinearCoding-master/data/mad-fingerprinting/'
src_np_path = ro + 'noiseprint/'
src_prnu_path = ro + 'prnu/'

acc_path = '/home/na/1_MAD/2_Data/6_few_shot_fingerprint_data/3_np_prnu_avg2/2_for_APL/'
folder_list = ['1_FRLL', '2_FERET', '3_FRGC', '4_CelebA', '5_self', '6_all']
sets = ['1_shot_train', '5_shot_train', 'test']

dst_path = ro + 'few_shot_fingerprint/'
dst_np_path = dst_path + 'noiseprint/'
dst_prnu_path = dst_path + 'prnu/'

for p in range(len(folder_list)):
    if p != 4: continue
    fold = folder_list[p]
    print(fold)
    for set in sets:
        print(set)
        ft = open(dst_path + fold + '_' + set + '_list.txt', 'w')
        count1 = 0
        ids = os.listdir(acc_path + fold + '/' + set)
        for id in ids:
            print(id)
            dst_np = dst_np_path + fold + '/' + set + '/' + id
            if os.path.exists(dst_np) is False: os.makedirs(dst_np)
            dst_prnu = dst_prnu_path + fold + '/' + set + '/' + id
            if os.path.exists(dst_prnu) is False: os.makedirs(dst_prnu)

            img_list = os.listdir(acc_path + fold + '/' + set + '/' + id)
            for img in img_list:
                for path, subdirs, files in os.walk(ro + 'noiseprint/' + id):
                    for name in files:
                        # print(os.path.join(path, name))
                        # if fold == '5_self' and
                        #     img = img.split('.')[0] + '.jpg'
                        if name == img:
                            pp = path.split('/')[-1]
                            s1 = src_np_path + id + '/' + pp + '/' + name
                            d1 = dst_np + '/' + name
                            shutil.copy(s1,d1)
                            s2 = src_prnu_path + id + '/' + pp + '/' + name
                            d2 = dst_prnu + '/' + name
                            shutil.copy(s2, d2)

                            img1 = 'noiseprint/' + fold + '/' + set + '/' + id + '/' + name
                            img2 = 'prnu/' + fold + '/' + set + '/' + id + '/' + name
                            lab = int(id)
                            ft.write(img1 + ' ' + img2 + ' ' + str(lab) + '\n')
                            count1 += 1
                            continue




        print('train=' + str(count1))
        ft.close()




