img = imread('btest.bmp');


% img_out = original_img;
% for k = 1 : length(stats) 
%     thisBB = stats(k).BoundingBox;
%     f = @() rectangle('Position', [thisBB(1),thisBB(2),thisBB(3),thisBB(4)]);
%     params = {{'EdgeColor','r','LineWidth',2}};
%     img_out = insertInImage(img_out,f,params);
% end
% 
% imwrite(img_out,'eyes_detected/ori.bmp');
% figure();imshow(imread('eyes_detected/ori.bmp'));