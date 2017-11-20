img = imread('img/pattern.bmp');
salt_img = imnoise(img,'salt & pepper',0.2);
%gaussian_img = imnoise(img,'gaussian',0,0);
%figure,image(salt_img),axis off,colormap gray(256);
%figure,image(gaussian_img),axis off,colormap gray(256);
%figure,image(img),axis off,colormap gray(256);

mask = fspecial('average',7);
box_filtered_img = filter2(mask,salt_img);
gaussian_mask = fspecial('gaussian',7);
gaussian_filtered_img = filter2(gaussian_mask,salt_img);
filtered_img = medfilt2(salt_img,[5,5]); 

figure,image(filtered_img),axis off,colormap gray(256),title('median');
figure,image(box_filtered_img),axis off,colormap gray(256),title('box filter');
figure,image(gaussian_filtered_img),axis off,colormap gray(256),title('gaussian filter image');
figure,image(salt_img),axis off,colormap gray(256),title('noised image');
