function img = auto_threshold( img )
%AUTO_THRESHOLD Summary of this function goes here
%   Detailed explanation goes here
    threshold = mean(img(:));
    img(img<threshold) = 0;
    img(img>threshold) = 256;

end

