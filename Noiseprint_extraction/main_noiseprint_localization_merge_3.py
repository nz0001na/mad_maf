# This is the code to extract Noiseprint, and blind localization

from noiseprint.noiseprint import genNoiseprint
from noiseprint.utility.utilityRead import imread2f
from noiseprint.utility.utilityRead import jpeg_qtableinv
from noiseprint.noiseprint_blind import noiseprint_blind_file
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import io
import os
import gc


src_path = '/'
dst_path = '/'
# dst_fig_path = dst_path + 'figure/'
# if os.path.exists(dst_fig_path) is False:
#     os.makedirs(dst_fig_path)
dst_noise_path = dst_path + 'noiseprint/'
if os.path.exists(dst_noise_path) is False:
    os.makedirs(dst_noise_path)
# dst_heatmap_path = dst_path + 'heatmap/'
# if os.path.exists(dst_heatmap_path) is False:
#     os.makedirs(dst_heatmap_path)

folder_list = os.listdir(src_path)
for i in range(len(folder_list)):
    folder = folder_list[i]
    print(folder)
    # if os.path.exists(dst_fig_path + folder + '/') is False:
    #     os.makedirs(dst_fig_path + folder + '/')
    if os.path.exists(dst_noise_path + folder + '/') is False:
        os.makedirs(dst_noise_path + folder + '/')
    # if os.path.exists(dst_heatmap_path + folder + '/') is False:
    #     os.makedirs(dst_heatmap_path + folder + '/')

    img_list = os.listdir(src_path + folder + '/')
    for j in range(len(img_list)):
        img_name = img_list[j]
        imgfile = src_path + folder + '/' + img_name

        # noiseprint extraction
        img, mode = imread2f(imgfile, channel=1)
        QF = 200
        res = genNoiseprint(img, QF)
        out_dict = dict()
        out_dict['noiseprint'] = res
        out_dict['QF'] = QF

        # save noiseprint
        sio.savemat(dst_noise_path + folder + '/' + img_name[:len(img_name)-3] + 'mat', out_dict)

        # # heatmap
        # with open(imgfile, 'rb') as f:
        #     stream = io.BytesIO(f.read())
        # QF, mapp, valid, range0, range1, imgsize, other = noiseprint_blind_file(imgfile)
        # if mapp is None:
        #     print('Image is too small or too uniform')
        # out_dict = dict()
        # out_dict['QF'] = QF
        # out_dict['map'] = mapp
        # out_dict['valid'] = valid
        # out_dict['range0'] = range0
        # out_dict['range1'] = range1
        # out_dict['imgsize'] = imgsize
        # out_dict['other'] = other
        #
        # sio.savemat(dst_heatmap_path + folder + '/' + img_name[:len(img_name)-3] + 'mat', out_dict)

        # # show figure
        # img, mode = imread2f(imgfile, channel=3)
        # vmin = np.min(res[34:-34, 34:-34])
        # vmax = np.max(res[34:-34, 34:-34])
        #
        # plt.figure(figsize=(3 * 5, 2 * 5))
        # grid = gridspec.GridSpec(2, 3, wspace=0.2, hspace=0.2, )
        # plt.subplot(grid[0, 0])
        # plt.imshow(img, clim=[0, 1])
        # plt.title('Input image')
        # plt.subplot(grid[0, 1])
        # plt.imshow(res.clip(vmin, vmax), clim=[vmin, vmax], cmap='gray') # cmap='gray', 'inferno'
        # plt.title('noiseprint')
        # plt.subplot(grid[0, 2])
        # plt.imshow(mapp, clim=[np.nanmin(mapp), np.nanmax(mapp)], cmap='jet')
        # plt.title('Heatmap')
        # # plt.show()
        # plt.savefig(dst_fig_path + folder + '/' + img_name[:len(img_name)-3] + 'jpg', bbox_inches='tight')
        # plt.close()
        # gc.collect()
