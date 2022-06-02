# This is the code to extract Noiseprint
#    python main_extraction.py input.png noiseprint.mat
#    python main_showout.py input.png noiseprint.mat
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Copyright (c) 2019 Image Processing Research Group of University Federico II of Naples ('GRIP-UNINA').
# All rights reserved.
# This work should only be used for nonprofit purposes.
#
# By downloading and/or using any of these files, you implicitly agree to all the
# terms of the license, as specified in the document LICENSE.txt
# (included in this package) and online at
# http://www.grip.unina.it/download/LICENSE_OPEN.txt
#

from sys import argv
from time import time
from noiseprint.noiseprint import genNoiseprint
from noiseprint.utility.utilityRead import imread2f
from noiseprint.utility.utilityRead import jpeg_qtableinv
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

imgfilename = 'example/paper/fake4.png'
# outfilename = 'example/paper/morph3.mat'

timestamp = time()
img, mode = imread2f(imgfilename, channel=1)
QF = 200
res = genNoiseprint(img, QF)

# timeApproach = time() - timestamp
out_dict = dict()
out_dict['noiseprint'] = res
out_dict['QF'] = QF
# out_dict['time'] = timeApproach

# save noiseprint
# sio.savemat(outfilename, out_dict)
# np.savez(outfilename, **out_dict)

# show noiseprint
print(' %s' % imgfilename)
img, mode = imread2f(imgfilename, channel=3)
print('size : ', img.shape)
# print('time : %g' % time)
# print('qf   : %g' % QF)

vmin = np.min(res[34:-34, 34:-34])
vmax = np.max(res[34:-34, 34:-34])

plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(img, clim=[0, 1])
plt.title('input \n image (%s, %d)' % (mode,QF))
plt.subplot(1, 2, 2)
plt.imshow(res.clip(vmin, vmax), clim=[vmin, vmax], cmap='gray') # cmap='gray', 'inferno'
plt.title('noiseprint')
plt.show()