function img =  gamma_transform( img,gamma )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    
    img = double(img);
    img = 255.*(img./255).^(1./gamma);%Equation on Blackboard is wrong
    img = uint8(img);
    
end