
function [] = display_image_channels( img )
%DISPLAY_IMAGE_CHANNELS Summary of this function goes here
%   Detailed explanation goes here
figure(),imshow(img(:,:,1)),title('RED');
figure(),imshow(img(:,:,2)),title('GREEN');
figure(),imshow(img(:,:,3)),title('BLUE');
end

