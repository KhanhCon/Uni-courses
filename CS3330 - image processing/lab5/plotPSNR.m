
img = imread('img/pattern.bmp');
salt_img = imnoise(img,'salt & pepper',0.2);
gau3 = filter2(fspecial('average',3),salt_img);
PSNR_gau3 = calculatePSNR(salt_img,gau3);
gau5 = filter2(fspecial('average',5),salt_img);
PSNR_gau5 = calculatePSNR(salt_img,gau5);
gau7 = filter2(fspecial('average',7),salt_img);
PSNR_gau7 = calculatePSNR(salt_img,gau7);
gau9 = filter2(fspecial('average',9),salt_img);
PSNR_gau9 = calculatePSNR(salt_img,gau9);
gau11 = filter2(fspecial('gaussian',11),salt_img);
PSNR_gau11 = calculatePSNR(salt_img,gau11);


figure,image(salt_img),axis off,colormap gray(256);
figure,image(gau11),axis off,colormap gray(256);