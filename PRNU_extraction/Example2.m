addpath(strcat(pwd,'\Functions'))
addpath(strcat(pwd,'\Filter'))

imx = 'Images\002_03_q55.jpg',
Noisex = NoiseExtractFromImage(imx,2);
imshow(Noisex)
Noisex = WienerInDFT(Noisex,std2(Noisex));
imshow(Noisex)