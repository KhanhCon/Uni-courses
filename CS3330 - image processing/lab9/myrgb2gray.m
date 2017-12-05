function [ gray_img ] = myrgb2gray( color_img )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    gray_img = uint8((0.299*double(color_img(:,:,1))+0.587*double(color_img(:,:,2))+0.114*double(color_img(:,:,3))));
    
end

