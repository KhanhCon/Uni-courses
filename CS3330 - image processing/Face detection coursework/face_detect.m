
%figure(),imshow(img);
%resize 300×225

%ycbcr = myrgb2ycbcr(img);
%gray = rgb2gray(ycbcr);
%resized = imresize(gray,[225 300]);
%figure(),imshow(resized);

%edge_img = my_canny(resized,100,50);  
%edge_img = edge(resized,'sobel');%use it for now
%figure(),imshow(edge_img);

%{
%Image 
img = rgb2gray(imread('img/original.png'));
%Apple sobel edge detection
edge_img = edge(img,'sobel');
figure();imshow(edge_img);title('whiteface');

SE = strel('disk', 3);
SE_diamond = strel('diamond', 3);

%dilated diamon
dilated_img = imdilate(edge_img,SE);
white_filled_img = imfill(dilated_img,'holes');
figure();imshow(white_filled_img);title('whiteface');

[rows,cols] = size(white_filled_img);
top_col = 0;
for row = 20:rows
    br = 1;
    for col = 1:cols/2

        if white_filled_img(row,col) == 1
             top_col = col;
%              hold on;
%              plot(row,col, 'b*');
%                hold off;
               br = 2;
               break;
        end
    
     end
         if br == 2
            break
    end
end 
[rows,cols] = size(white_filled_img);
ear_row = 0;
for col = 1:cols
    br = 1;
    for row = 1:rows
        rectangle('Position',[row col 3 3],'EdgeColor','r')
        drawnow
        col
        if white_filled_img(row,col) == 1
            ear_row = row
            br = 2
            break
        end
    end
    if br == 2
        break
    end
end 
% face_center = I(top_row,top_col);
hold on
plot(top_row,top_col, 'r*')
hold off



% final_CC = bwconncomp(white_filled_img,4); %%final image
% stats1 = regionprops(final_CC,'all');
% for k = 1 : length(stats1) 
%   thisBB = stats1(k).BoundingBox; 
%   rectangle('Position', [thisBB(1),thisBB(2),thisBB(3),thisBB(4)], 'EdgeColor','r','LineWidth',2 ); 
% end

% s = regionprops(white_filled_img,'centroid');
% 
% centroids = cat(1, s.Centroid);
% hold on
% plot(centroids(:,1),centroids(:,2), 'b*')
% hold off

morphological_closed_img = imclose(dilated_img,SE_diamond);
eroded_img = imerode(morphological_closed_img,SE);

figure();imshow(morphological_closed_img);title('eroded');
%}
%Image 
img_template = rgb2gray(imread('img/original.png'));
hist = imhist(img_template);
img = rgb2gray(imread('face/gillian1.jpg'));
img = histeq(img);
 figure();imshow(img);title('improve contrast');
%Apple sobel edge detection
edge_img = edge(img,'sobel');
SE = strel('disk', 3);
%Dilate the image twice
dilated_img = imdilate(edge_img,SE);
dilated_img2 = imdilate(dilated_img,SE);
%figure();imshow(dilated_img2);title('dilated');
%dilated_img2 = imdilate(dilated_img2,SE);
%Inverse image to fill holes then inverse it back
negative_dilated_img = imcomplement(dilated_img2);
CC = bwconncomp(negative_dilated_img,4);
stats_first = regionprops(CC,'Area');
idx = find([stats_first.Area] > 300); 
filled_img = imcomplement(ismember(labelmatrix(CC), idx));
%figure();imshow(filled_img);
% CC_test = bwconncomp(filled_img_first,4);
% stats_test = regionprops(CC_test,'Area');
% 
% idx_test = find([stats_test.Area] > 500);
% filled_img = ismember(labelmatrix(CC_test), idx_test);
% 
 


%Erode image three times
eroded_img = imerode(filled_img,SE);
eroded_img2 = imerode(eroded_img,SE);
eroded_img3 = imerode(eroded_img2,SE);
eroded_img4 = imerode(eroded_img3,SE);
eroded_img5 = imerode(eroded_img4,SE);


% figure();imshow(eroded_img3),title('erode');

%Apple rules
eroded3_CC = bwconncomp(eroded_img3,4);
eroded3_stats = regionprops(eroded3_CC,'all');
    
  %Aspect ratio rule
 idx_boundingbox = [];
 for k = 1 : length(eroded3_stats) 
     thisBB = eroded3_stats(k).BoundingBox; 
     aspect_ratio = thisBB(3)/thisBB(4);
     if aspect_ratio > 0.8 && aspect_ratio < 4.0
         idx_boundingbox = [idx_boundingbox k];
     end
 end

aspect_ratio_img = ismember(labelmatrix(eroded3_CC), idx_boundingbox);
% figure(),imshow(aspect_ratio_img);


    %The orientation angle of eyes is not greater than 45 degrees.
angle_img_CC = bwconncomp(aspect_ratio_img,4);
stats = regionprops(angle_img_CC,'Orientation');
angle_idx = find([stats.Orientation] <= 45); 
angle_img = ismember(labelmatrix(angle_img_CC), angle_idx);
%figure(),imshow(angle_img),title('angle');
    
    %remove small component
CC_rm2 = bwconncomp(angle_img,4);
stats_rm2 = regionprops(CC_rm2,'Area');
idx_rm2 = find([stats_rm2.Area] > 50); 
rm2_img = ismember(labelmatrix(CC_rm2), idx_rm2);
%figure(),imshow(rm2_img),title('rm2');

    %no large than twice
size_img_CC = bwconncomp(rm2_img,4);
size_img_stats = regionprops(size_img_CC,'all');
% bb1 = size_img_stats(2).BoundingBox; 
% rectangle('Position', [bb1(1),bb1(2),bb1(3),bb1(4)], 'EdgeColor','r','LineWidth',2 ); 

idx_size = [];
[y,x] = size(angle_img);
 for i = 1 : length(size_img_stats) 
     thisCentroid1 = size_img_stats(i).Centroid;
     thisBB = size_img_stats(i).BoundingBox;
     thisArea = size_img_stats(i).Area;
     thisOrientation = size_img_stats(i).Orientation;
     padding = 60.0;
     padding_top = 80.0;
     for  i2 = 1:length(size_img_stats) 
        
        bb2 = size_img_stats(i2).BoundingBox;
        center1 = [thisBB(1)+thisBB(3)/2,thisBB(2)+thisBB(4)/2 ];
        center2 = [bb2(1)+bb2(3)/2, bb2(2)+bb2(4)/2];
        slope_angle = atan2(center2(2)-center1(2),center2(1)-center1(1))* 180/pi;
        slope_angle = abs(slope_angle);
        if slope_angle >  90.0
            slope_angle = 180.0 - slope_angle;
        end
%       slope_angle = (tan(line1)-tan(line2))/(1+tan(line1)*tan(line2));
        ratio = thisArea/size_img_stats(i2).Area;
        orient_diff = thisOrientation - size_img_stats(i2).Orientation;
%         slope_angle = (atan((thisCentroid1(2)-thisCentroid1(1))/(thisCentroid1(2)-thisCentroid1(1))) - atan((3-1)/(3-0))) * 180/pi
        if thisBB(1) > size_img_stats(i2).BoundingBox(1)
           distance = (thisBB(1) + thisBB(3)) - size_img_stats(i2).BoundingBox(1);
        else
            distance =  size_img_stats(i2).BoundingBox(1) + size_img_stats(i2).BoundingBox(3)-thisBB(1);
        end
        if ratio > 0.5 && ratio < 2.0 && abs(orient_diff) < 30.0 && padding<thisBB(1) && thisBB(1)+thisBB(3)<x-padding  && padding_top<thisBB(2)&& thisBB(2)+thisBB(4)<y -padding_top && abs(distance) > 10  && slope_angle < 20.0
            
            idx_size = [idx_size i];
            break;
        end
     end
 end
size_img = ismember(labelmatrix(size_img_CC), idx_size);
figure(),imshow(size_img),title('all');

final_CC = bwconncomp(size_img,4); %%final image
%L = labelmatrix(final_CC);
final_stats = regionprops(final_CC,'all');
for k = 3 : 3 
    thisBB = final_stats(k).BoundingBox; 
    rectangle('Position', [thisBB(1),thisBB(2),thisBB(3),thisBB(4)], 'EdgeColor','r','LineWidth',2 ); 
end


    %orientation difference
orient_diff_CC = bwconncomp(size_img,4);
orient_diff_stats = regionprops(orient_diff_CC,'All');
idx_orient_diff = [];
thisBB = orient_diff_stats(1).BoundingBox;
bb2 = size_img_stats(3).BoundingBox;
center1 = [thisBB(1)+thisBB(3)/2,thisBB(2)+thisBB(4)/2 ];
center2 = [bb2(1)+bb2(3)/2, bb2(2)+bb2(4)/2];
line([center1(1) center2(1)],[center1(2) center2(2)])
line([size_img_stats(1).Centroid(1) size_img_stats(3).Centroid(1)],[size_img_stats(1).Centroid(2) size_img_stats(3).Centroid(2)])
slope_angle = atan2(center2(2)-center1(2),center2(1)-center1(1))* 180/pi
slope_angle = abs(slope_angle);
if slope_angle > 90.0
    slope_angle = 180.0 - slope_angle
end


 for j = 1 : length(orient_diff_stats) 
      thisBB = orient_diff_stats(j).BoundingBox;
      thisCentroid1 = size_img_stats(j).Centroid;  
      for  j2 = 1:length(orient_diff_stats) 
         thisCentroid2 = size_img_stats(j2).Centroid;
        
        bb2 = size_img_stats(i2).BoundingBox;
         center1 = [thisBB(1)+thisBB(3)/2,thisBB(2)+thisBB(4)/2 ];
         center2 = [bb2(1)+bb2(3)/2, bb2(2)+bb2(4)/2];
         slope_angle = atan2(center2(2)-center1(2),center2(1)-center1(1))* 180/pi;
        
         line([center1(1) center2(1)],[center1(2) center2(2)])
         
      end
  end
orient_diff_img = ismember(labelmatrix(orient_diff_CC), idx_orient_diff);
%figure(),imshow(orient_diff_img),title('orient diff');



% centers = stats1.BoundingBox;
% diameters = mean([stats1.MajorAxisLength stats1.MinorAxisLength],2);
% radii = diameters/2;
% 
% % hold on
% % viscircles(centers,radii);
% % hold off

%TEST draw box. use it with regionpops(final_image,..)..
% final_CC = bwconncomp(eroded_img3,4); %%final image
% L = labelmatrix(final_CC);
% stats1 = regionprops(final_CC,'all');
% for k = 1 : length(stats1) 
%     thisBB = stats1(k).BoundingBox; 
%     rectangle('Position', [thisBB(1),thisBB(2),thisBB(3),thisBB(4)], 'EdgeColor','r','LineWidth',2 ); 
% end

% bb1 = stats1(2).BoundingBox; 
% rectangle('Position', [bb1(1),bb1(2),bb1(3),bb1(4)], 'EdgeColor','r','LineWidth',2 ); 
% rectangle('Position', [bb1(1),bb1(2),bb1(4),bb1(4)], 'EdgeColor','r','LineWidth',2 ); 
% aaaaa = bb1(1);
% w =  bb1(3);
% h =  bb1(4);

% negative_dilated_img = imcomplement(dilated_img);
% %figure();imshow(negative_dilated_img);
% CC1 = bwconncomp(dilated_img,4);
% numPixels = cellfun(@numel,CC1.PixelIdxList);
% %[k,idk] = numPixels{18};
% [biggest,idx] = max(numPixels);
% %negative_dilated_img(CC.PixelIdxList{idx}) = 0;
% figure();imshow(negative_dilated_img);
% CC = bwconncomp(negative_dilated_img,4);
% L = labelmatrix(CC);
% stats = regionprops(CC,'All');
% idx = find([stats.Area] > 100); 
% filled_img = ismember(labelmatrix(CC), idx);  
% %figure();imshow(biggest);
% %figure();imshow(stats(1).Image);
% 
% filled_dilated_img = imfill(dilated_img,'holes');
% 
% %areas = stats(Area<4);
% %figure();imshow(negative_dilated_img);
% figure();imshow(imcomplement(filled_img));
% filled_img2 = imcomplement(filled_img);
% CC2 = bwconncomp(filled_img2,4);
% 
% stats2 = regionprops(CC,'All');

