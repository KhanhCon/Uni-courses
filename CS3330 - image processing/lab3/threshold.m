function img = threshold( img,threshold )
%THRESHOLD Summary of this function goes here
%   Detailed explanation goes here
    img(img<threshold) = 0;
    img(img>=threshold) = 256;
end

%threshold after inspecting imhist(img) is (20+202)/2=111 