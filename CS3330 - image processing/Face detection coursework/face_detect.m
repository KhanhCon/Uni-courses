img = imread('img/original.png');
figure(),imshow(img);
%resize 300×225

ycbcr = myrgb2ycbcr(img);
gray = rgb2gray(ycbcr);
resized = imresize(gray,[225 300]);
figure(),imshow(resized);

edge_img = my_canny(resized,100,50);  
%edge_img = edge(resized,'sobel');%use it for now
figure(),imshow(edge_img);

