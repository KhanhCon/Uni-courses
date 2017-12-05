function [grad_mag,grad_dir ] = calculate_gradient( img )
%CALCULATE_GRADIENT Summary of this function goes here
%   Detailed explanation goes here
    imgdbl = double(img);
    maskx = [-1 0 1;-2 0 2;-1 0 1];
    masky = [-1 -2 -1;0 0 0;1 2 1];
    resX = conv2(imgdbl, maskx);
    resY = conv2(imgdbl, masky);
    
    grad_mag = sqrt(resX.^2 + resY.^2);
    grad_dir = atan(resY/resX);
    
end

