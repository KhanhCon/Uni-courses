function [ sharpen_img ] = sharpen_img( img )
%SHARPEN_IMG Summary of this function goes here
%   Detailed explanation goes here
%img = rgb2gray(img);

laplacian = [0,1,0;1,-4,1;0,1,0];
laplacian_img = filter2(laplacian,img);

sharpen_img = img - uint8(laplacian_img);

figure,image(sharpen_img),axis off,colormap gray(256),title('sharpen');
figure,image(img),axis off,colormap gray(256),title('original');
end

