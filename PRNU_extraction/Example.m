% Camera identification example

addpath(strcat(pwd,'\Functions'))
addpath(strcat(pwd,'\Filter'))
%       image_directory = '\TestImages';
%       Images = dir([image_directory,'\*.jpg']);
%       addpath(image_directory)
%       [RP,LP,ImagesinRP] = getFingerprint(Images);


%'Example - Do the three images represent the same camera that took the image Pxxx.jpg?'
im1 = 'Images\001_03_020_03_alpha0.5_combined_morph_q32.jpg'
% im2 = 'Images\P2.jpg',
% im3 = 'Images\P3.jpg',
Images(1).name = im1;  
% Images(2).name = im2; 
% Images(3).name = im3; 
RP = getFingerprint(Images);
imshow(RP)
RP = rgb2gray1(RP);
sigmaRP = std2(RP);
Fingerprint = WienerInDFT(RP,sigmaRP);
imshow(Fingerprint)

imx = 'Images\001_03_020_03_alpha0.5_combined_morph_q32.jpg',
Noisex = NoiseExtractFromImage(imx,2);
imshow(Noisex)
Noisex = WienerInDFT(Noisex,std2(Noisex));
imshow(Noisex)

% The optimal detector (see publication "Large Scale Test of Sensor Fingerprint Camera Identification")
Ix = double(rgb2gray(imread(imx)));
C = crosscorr(Noisex,Ix.*Fingerprint);
detection = PCE(C)

