img = imread('demo_face/gordon3.jpg');
%grey img
grey_img = rgb2gray(img);
imwrite(grey_img, 'report/grey.jpg');
%edge img
edge_img = edge(grey_img,'sobel');
imwrite(edge_img, 'report/edge.jpg');

%Dilate the image twice
SE = strel('disk', 3);
dilated_img = imdilate(edge_img,SE);
dilated_img = imdilate(dilated_img,SE);
imwrite(dilated_img, 'report/dilated.jpg');


%negative dilated img with holes
negative_dilated_img = imcomplement(dilated_img);
imwrite(negative_dilated_img, 'report/Negative image with holes.jpg');

% Negative Image With Holes filled
CC = bwconncomp(negative_dilated_img,4);
stats_first = regionprops(CC,'Area');
idx = find([stats_first.Area] > 300); 
ne_img_with_holes = ismember(labelmatrix(CC), idx);
imwrite(ne_img_with_holes, 'report/Negative image with holes filled.jpg');
% Final Image With Holes Filled 
filled_img = imcomplement(ne_img_with_holes);
imwrite(filled_img, 'report/Final Image With Holes Filled .jpg');


%Right eye with holes
right_eye_holes = dilated_img(230:280,120:200,:);
imwrite(right_eye_holes, 'report/Right eye with holes.jpg');
%Right eye with holes filled
right_eye_holes_filled = filled_img(230:280,120:200,:);
imwrite(right_eye_holes_filled, 'report/Right eye with holes filled.jpg');

%Erode image three times
eroded_img = imerode(filled_img,SE);
eroded_img = imerode(eroded_img,SE);
eroded_img = imerode(eroded_img,SE);
imwrite(eroded_img, 'report/Eroded Image .jpg');

%Eyes detect
% imwrite(eyes_detect(imread('demo_face/jsheenan3.jpg')), 'report/eyes_detect1.jpg');
% imwrite(eyes_detect(imread('demo_face/martin4.jpg')), 'report/eyes_detect2.jpg');
% imwrite(eyes_detect(imread('demo_face/catherine2.jpg')), 'reportstats_first/eyes_detect3.jpg');
% imwrite(eyes_detect(imread('demo_face/gordon3.jpg')), 'report/eyes_detect4.jpg');
% imwrite(eyes_detect(imread('demo_face/jim18.jpg')), 'report/eyes_detect5.jpg');
% imwrite(eyes_detect(imread('demo_face/kay11.jpg')), 'report/eyes_detect6.jpg');
% imwrite(eyes_detect(imread('demo_face/kirsty17.jpg')), 'report/eyes_detect7.jpg');
% imwrite(eyes_detect(imread('demo_face/louise11.jpg')), 'report/eyes_detect8.jpg');

% clipped = img(180:250,110:200,:);
% imshow(clipped);
