% Code for PRNU extraction
addpath(strcat(pwd,'\Functions'))
addpath(strcat(pwd,'\Filter'))

src_path = '\'
dst_path = '\'

   
if ~exist([dst_path 'image\'], 'dir')
    mkdir([dst_path 'image\'])
end

if ~exist([dst_path 'matrix\'], 'dir')
    mkdir([dst_path 'matrix\'])
end
    
Images = dir([src_path, '\*.png']);
len = size(Images,1)
for j=1:len
    img_name = Images(j).name
    imx = [src_path img_name]
    Noisex = NoiseExtractFromImage(imx,2);
%         imshow(Noisex)
    Noisex = WienerInDFT(Noisex,std2(Noisex));
%         imshow(Noisex)
    imwrite(Noisex, [dst_path 'image\' img_name])
    a = strsplit(img_name,'.')
    new_name = [a{1} '.mat']
    save([dst_path 'matrix\' new_name],'Noisex')

end
    
    
