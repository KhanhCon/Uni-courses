
img = imread('img/pattern.bmp');
salt_img = imnoise(img,'salt & pepper',0.2);
gau3 = filter2(fspecial('gaussian',3),salt_img);
PSNR_gau3 = calculatePSNR(salt_img,gau3);
gau5 = filter2(fspecial('gaussian',5),salt_img);
PSNR_gau5 = calculatePSNR(salt_img,gau5);
gau7 = filter2(fspecial('gaussian',7),salt_img);
PSNR_gau7 = calculatePSNR(salt_img,gau7);
gau9 = filter2(fspecial('gaussian',9),salt_img);
PSNR_gau9 = calculatePSNR(salt_img,gau9);
gau11 = filter2(fspecial('gaussian',11),salt_img);
PSNR_gau11 = calculatePSNR(salt_img,gau11);

x = 3:2:11;
y = [PSNR_gau3,PSNR_gau5,PSNR_gau7,PSNR_gau9,PSNR_gau11];

%figure,plot(x,y);

PSNR_box3 = calculatePSNR(salt_img,filter2(fspecial('average',3),salt_img));
PSNR_box5 = calculatePSNR(salt_img,filter2(fspecial('average',5),salt_img));
PSNR_box7 = calculatePSNR(salt_img,filter2(fspecial('average',7),salt_img));
PSNR_box9 = calculatePSNR(salt_img,filter2(fspecial('average',9),salt_img));
PSNR_box11 = calculatePSNR(salt_img,filter2(fspecial('average',11),salt_img));

y2 = [PSNR_box3,PSNR_box5,PSNR_box7,PSNR_box9,PSNR_box11];
%figure,plot(x,y2);

PSNR_med3 = calculatePSNR(medfilt2(salt_img,[3,3]),salt_img);
PSNR_med5 = calculatePSNR(salt_img,medfilt2(salt_img,[5,5]));
PSNR_med7 = psnr(salt_img,medfilt2(salt_img,[7,7]));
PSNR_med9 = psnr(salt_img,medfilt2(salt_img,[9,9]));
PSNR_med11 = psnr(medfilt2(salt_img,[11,11]),salt_img);

y3 = [PSNR_med3,PSNR_med5,PSNR_med7,PSNR_med9,PSNR_med11];
figure,plot(x,y3);

