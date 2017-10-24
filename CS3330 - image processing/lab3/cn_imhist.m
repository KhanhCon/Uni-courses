function h = cn_imhist(img)
%CN_IMHIST Summary of this function goes here
%   Detailed explanation goes here
    
    h = imhist(img);
    h = h/norm(h);
    h = cumsum(h);

end

