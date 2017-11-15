img = imread('img/pattern.bmp');
mask = fspecial('average',7);
box_filtered_img = filter2(mask,img);
filtered_img = medfilt2(img,[7,7]); 
figure,image(filtered_img),axis off,colormap gray(256);
figure,image(box_filtered_img),axis off,colormap gray(256);
figure,image(img),axis off,colormap gray(256);






