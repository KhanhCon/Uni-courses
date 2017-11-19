function [ point_detected_img ] = point_detection( img )
%POINT_DETECTION Summary of this function goes here
%   Detailed explanation goes here
mask = [-1,-1,-1;-1,8,-1;-1,-1,-1];
point_detected_img = filter2(mask,rgb2gray(img));
point_detected_img(point_detected_img<255) = 0;
figure,image(point_detected_img),axis off,colormap gray(256),title('point detection');

end

