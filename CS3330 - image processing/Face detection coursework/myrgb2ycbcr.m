
function [ ycbcr_img ] = myrgb2ycbcr( color_img )
%MYRGB2YCBCR Summary of this function goes here
%   Detailed explanation goes here
    Y = 0.299*double(color_img(:,:,1))+0.586*double(color_img(:,:,2))+0.114*double(color_img(:,:,3));
    Cb = -0.169*double(color_img(:,:,1))-0.331*double(color_img(:,:,2))+0.449*double(color_img(:,:,3));
    Cr = 0.499*double(color_img(:,:,1))-0.418*double(color_img(:,:,2))-0.0813*double(color_img(:,:,3)); 
    
    %gray_img = double(Y + Cb +Cr);
    %gray_img = rgb2ycbcr(color_img);
    %gray_img = color_img;
    ycbcr_img(:,:,1) = uint8(Y);
    ycbcr_img(:,:,2) = uint8(Cb);
    ycbcr_img(:,:,3) = uint8(Cr);
    
    
end

