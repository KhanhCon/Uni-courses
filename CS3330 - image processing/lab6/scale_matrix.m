function [ img ] = scale_matrix( M )
%SCALE_MATRIX Summary of this function goes here
%   Detailed explanation goes here
new_max = 255;
new_min = 0;

current_max = max(M(:));
current_min = min(M(:));

scaled_double_matrix =((M-current_min)*(new_max-new_min))/(current_max-current_min) + new_min;
img = uint8(scaled_double_matrix);

end

