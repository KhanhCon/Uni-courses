
function [ PSNR ] = calculatePSNR( img1,img2 )
%CALCULATEPSNR Summary of this function goes here
%   Detailed explanation goes here
diff = double(img1) - double(img2);
diff = diff.^2;
diff = sum(diff(:));
MSE = diff./(size(img1,1)*size(img1,2)); % 256*256
PSNR = 10*log10(255.^2./MSE);

end

