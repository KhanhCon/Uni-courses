img = imread('btest.bmp');
original_img = imread('face/gillian1.jpg');
CC = bwconncomp(img,4); %%final image
stats = regionprops(CC,'all');

figure();imshow(img);
idx_size = [];
for k1 = 1 : length(stats) 
    BB1 = stats(k1).BoundingBox;
    Area1 = stats(k1).Area;
    for k2 = 1 : length(stats)
        if k1 == k2
            continue
        end
        BB2 = stats(k2).BoundingBox;
        center1 = [BB1(1)+BB1(3)/2,BB1(2)+BB1(4)/2 ];
        center2 = [BB2(1)+BB2(3)/2, BB2(2)+BB2(4)/2];
        slope_angle = atan2(center2(2)-center1(2),center2(1)-center1(1))* 180/pi;
        slope_angle = abs(slope_angle);
        if slope_angle >  90.0
            slope_angle = 180.0 - slope_angle;
        end
        
        line([center1(1) center2(1)],[center1(2) center2(2)]);
        Area2 = stats(k2).Area;
        ratio = Area1/Area2;
        
        orient_diff = stats(k1).Orientation - stats(k2).Orientation;
        
        if ratio > 0.5 && ratio < 2.0 && slope_angle < 45.0 && orient_diff<30.0
            idx_size = [idx_size k1 k2];
            break;
        end
%         rectangle('Position', [thisBB(1),thisBB(2),thisBB(3),thisBB(4)],'EdgeColor','r','LineWidth',2);
    end
end
final_img = ismember(labelmatrix(CC), idx_size);
figure(),imshow(final_img),title('all');

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