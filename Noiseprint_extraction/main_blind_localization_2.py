# This code is the main of the noiseprint_blind
#    python main_blind.py input.png output.mat
#    python main_showout.py input.png output.mat
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
import scipy.io as sio
from time import time
import io
from noiseprint.noiseprint_blind import noiseprint_blind_file
import numpy as np
import matplotlib.pyplot as plt
from noiseprint.utility.utilityRead import imread2f

imgfilename = 'example/fake3.png'
# outfilename = 'example/paper/_map.mat'

with open(imgfilename,'rb') as f:
    stream = io.BytesIO(f.read())
    
timestamp = time()
QF, mapp, valid, range0, range1, imgsize, other = noiseprint_blind_file(imgfilename)
timeApproach = time() - timestamp

if mapp is None:
    print('Image is too small or too uniform')

out_dict = dict()
out_dict['QF'     ] = QF
out_dict['map'    ] = mapp
out_dict['valid'  ] = valid
out_dict['range0' ] = range0
out_dict['range1' ] = range1
out_dict['imgsize'] = imgsize
out_dict['other'  ] = other
out_dict['time'   ] = timeApproach

# sio.savemat(outfilename, out_dict)
# np.savez(outfilename, **out_dict)

img, mode = imread2f(imgfilename, channel=3)
print('size : ', img.shape)

plt.figure()
plt.subplot(1,2,1)
plt.imshow(img, clim=[0, 1])
plt.title('Input image')
plt.subplot(1,2,2)
plt.imshow(mapp, clim=[np.nanmin(mapp), np.nanmax(mapp)], cmap='jet')
plt.title('Heatmap')
plt.show()
