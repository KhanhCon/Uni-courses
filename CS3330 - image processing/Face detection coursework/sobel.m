function [ edge_detected ] = sobel( img )
%SOBEL Summary of this function goes here
%   Detailed explanation goes here

%bw = uint8((1/3)*(double(img(:,:,1))+double(img(:,:,2))+double(img(:,:,3))));
%bw = uint8((0.299*double(img(:,:,1))+0.587*double(img(:,:,2))+0.114*double(img(:,:,3))));
%bw = rgb2gray(img);
bw =img;
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

%figure(),imshow(Gx);
masky = [1 2 1;0 0 0;-1 -2 -1];

for idx = 1:(r-3)
    for jdx = 1:(c-3)
        bwsquare = bwdbl(idx:(idx+2),jdx:(jdx+2));
        res = masky.*bwsquare;
        OUT(idx,jdx) = sum(sum(res));
    end
end
Gy = OUT;

%figure(),imshow(Gy);

%%% Normalise the results
%edge_detected = sqrt(Gx.^2 + Gy.^2);


resX = conv2(bwdbl, maskx);
resY = conv2(bwdbl, masky);
magnitude = sqrt(Gx.^2 + Gy.^2);
direction = atan(Gy/Gx);
thresh = magnitude < 101;
magnitude(thresh) = 0;
edge_detected = magnitude;
%figure(),imshow(edge_detected),title('edged');

end

