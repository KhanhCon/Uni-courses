img = rgb2gray(imread('img/original.png'));
%figure(),imshow(img);
%resize 300×225

%ycbcr = myrgb2ycbcr(img);
%gray = rgb2gray(ycbcr);
%resized = imresize(gray,[225 300]);
%figure(),imshow(resized);

%edge_img = my_canny(resized,100,50);  
%edge_img = edge(resized,'sobel');%use it for now
%figure(),imshow(edge_img);

%Apple sobel edge detection
edge_img = edge(img,'sobel');
SE = strel('disk', 3);

%Dilate the image twice
dilated_img = imdilate(edge_img,SE);
dilated_img2 = imdilate(dilated_img,SE);

%Inverse image to fill holes then inverse it back
negative_dilated_img = imcomplement(dilated_img2);
CC = bwconncomp(negative_dilated_img,4);
L = labelmatrix(CC);
stats = regionprops(CC,'All');
idx = find([stats.Area] > 100); 
filled_img = imcomplement(ismember(labelmatrix(CC), idx));

figure();imshow(filled_img);

%Erode image three times
eroded_img = imerode(filled_img,SE);
eroded_img2 = imerode(eroded_img,SE);
eroded_img3 = imerode(eroded_img2,SE);
eroded_img4 = imerode(eroded_img3,SE);
eroded_img5 = imerode(eroded_img4,SE);

figure();imshow(eroded_img3);

%Apple rules





% negative_dilated_img = imcomplement(dilated_img);
% %figure();imshow(negative_dilated_img);
% CC1 = bwconncomp(dilated_img,4);
% numPixels = cellfun(@numel,CC1.PixelIdxList);
% %[k,idk] = numPixels{18};
% [biggest,idx] = max(numPixels);
% %negative_dilated_img(CC.PixelIdxList{idx}) = 0;
% figure();imshow(negative_dilated_img);
% CC = bwconncomp(negative_dilated_img,4);
% L = labelmatrix(CC);
% stats = regionprops(CC,'All');
% idx = find([stats.Area] > 100); 
% filled_img = ismember(labelmatrix(CC), idx);  
% %figure();imshow(biggest);
% %figure();imshow(stats(1).Image);
% 
% filled_dilated_img = imfill(dilated_img,'holes');
% 
% %areas = stats(Area<4);
% %figure();imshow(negative_dilated_img);
% figure();imshow(imcomplement(filled_img));
% filled_img2 = imcomplement(filled_img);
% CC2 = bwconncomp(filled_img2,4);
% 
% stats2 = regionprops(CC,'All');

