img = imread('img/original.png');
figure(),imshow(img);
%resize 300×225
%gray = rgb2gray(img);
resized = imresize(img,[225 300]);
figure(),imshow(resized);

sobel(resized);
