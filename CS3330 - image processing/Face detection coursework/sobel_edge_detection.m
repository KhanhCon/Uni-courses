
original = imread('rubic.png');

%imshow(original)

clipped = original(:,1:550,:);

figure();
imshow(clipped);

% convert to grayscale

%bw = uint8((1/3)*(double(clipped(:,:,1))+double(clipped(:,:,2))+double(clipped(:,:,3))));
bw = rgb2gray(clipped);
figure(),imshow(bw)

bwdbl = double(bw);

maskx = [-1 -2 -1;0 0 0;1 2 1];
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

masky = [-1 0 1;-2 0 2;-1 0 1];
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
G = sqrt(Gx.^2 + Gy.^2);

figure(),imshow(G);

