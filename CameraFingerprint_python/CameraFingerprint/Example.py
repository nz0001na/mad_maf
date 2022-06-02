import src.Functions as Fu
import src.Filter as Ft
import src.getFingerprint as gF
import src.maindir as md
import src.extraUtils as eu
import numpy as np
import os
import cv2 as cv


# extracting Fingerprint from same size images in a path
im1 = 'Images'+os.sep+'P1.jpg'
im2 = 'Images'+os.sep+'P2.jpg'
im3 = 'Images'+os.sep+'P3.jpg'
Images = [im1, im2, im3]

RP,_,_ = gF.getFingerprint(Images)
RP = Fu.rgb2gray1(RP)
sigmaRP = np.std(RP)
Fingerprint = Fu.WienerInDFT(RP, sigmaRP)

# To save RP in a '.mat' file:
#import scipy.io as sio
#sio.savemat('Fingerprint.mat', {'RP': RP, 'sigmaRP': sigmaRP, 'Fingerprint': Fingerprint})

imx = 'Images'+os.sep+'Pxxx.jpg'
Noisex = Ft.NoiseExtractFromImage(imx, sigma=2.)
Noisex = Fu.WienerInDFT(Noisex, np.std(Noisex))

# The optimal detector (see publication "Large Scale Test of Sensor Fingerprint Camera Identification")
Ix = cv.cvtColor(cv.imread(imx),# image in BGR format
                 cv.COLOR_BGR2GRAY)

C = Fu.crosscorr(Noisex,np.multiply(Ix, Fingerprint))
det, det0 = md.PCE(C)
for key in det.keys(): print("{0}: {1}".format(key, det[key]))
eu.mesh(C)

