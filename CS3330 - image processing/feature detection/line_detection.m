function [ line_detected_img ] = line_detection( img,threshold )
%LINE_DETECTION Summary of this function goes here
%   Detailed explanation goes here
mask = [2,-1,-1;-1,2,-1;-1,-1,2];
line_detected_img = filter2(mask,rgb2gray(img));
line_detected_img(line_detected_img<threshold) = 0;
figure,image(line_detected_img),axis off,colormap gray(256),title('line detection');

end

