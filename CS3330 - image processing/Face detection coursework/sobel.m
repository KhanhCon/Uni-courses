function [ edge_detected ] = sobel( img )
%SOBEL Summary of this function goes here
%   Detailed explanation goes here

    bw = uint8((1/3)*(double(img(:,:,1))+double(img(:,:,2))+double(img(:,:,3))));
% bw = rgb2gray(clipped);
figure(),imshow(bw)

bwdbl = double(bw);

maskx = [-1 0 1;-2 0 2;-1 0 1];
[r,c] = size(bw);
OUT = zeros(r-3,c-3);
for idx = 1:(r-3)
    for jdx = 1:(c-3)
        bwsquare = bwdbl(idx:(idx+2),jdx:(jdx+2));
        res = maskx.*bwsquare;
        OUT(idx,jdx) = sum(sum(res));
    end
end
Gx = OUT;

figure(),imshow(Gx);
masky = [1 2 1;0 0 0;-1 -2 -1];

for idx = 1:(r-3)
    for jdx = 1:(c-3)
        bwsquare = bwdbl(idx:(idx+2),jdx:(jdx+2));
        res = masky.*bwsquare;
        OUT(idx,jdx) = sum(sum(res));
    end
end
Gy = OUT;

figure(),imshow(Gy);

%%% Normalise the results
%edge_detected = sqrt(Gx.^2 + Gy.^2);


resX = conv2(bwdbl, maskx);
resY = conv2(bwdbl, masky);
edge_detected = sqrt(Gx.^2 + Gy.^2);
direction = atan(Gy/Gx);
thresh = edge_detected < 101;
edge_detected(thresh) = 0;

figure(),imshow(edge_detected),label('edeged');

end

