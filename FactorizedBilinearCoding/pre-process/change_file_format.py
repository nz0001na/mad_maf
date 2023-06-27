import os
import cv2
from PIL import Image

ro = '/home/na/1_MAD/2_Data/6_few_shot_fingerprint_data/3_np_prnu_avg2/2_for_APL/5_self/test/'
src_path = ro + '7/'
dst_path = ro + '77/'
if os.path.exists(dst_path) is False:
    os.makedirs(dst_path)


img_list = os.listdir(src_path)
for q in range(len(img_list)):
    img = img_list[q].split('.')[0] + '.jpg'

    img_PIL = Image.open(src_path + img_list[q])
    # img_PIL.save(dst_path + img[0:len(img)-3] + 'jpg')
    img_PIL.save(dst_path + img)
    print('d')

