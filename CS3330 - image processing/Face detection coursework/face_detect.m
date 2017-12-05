img = rgb2gray(imread('img/original.png'));
%figure(),imshow(img);
%resize 300×225

%ycbcr = myrgb2ycbcr(img);
%gray = rgb2gray(ycbcr);
%resized = imresize(gray,[225 300]);
%figure(),imshow(resized);

edge_img = my_canny(resized,100,50);  
%edge_img = edge(resized,'sobel');%use it for now
%figure(),imshow(edge_img);


edge_img = edge(img,'sobel');
SE = strel('disk', 3);
dilated_img = imdilate(edge_img,SE);
dilated_img2 = imdilate(dilated_img,SE);
eroded_img = imerode(dilated_img2,SE);
eroded_img2 = imerode(eroded_img,SE);
eroded_img3 = imerode(eroded_img2,SE);

figure();imshow(eroded_img3);
