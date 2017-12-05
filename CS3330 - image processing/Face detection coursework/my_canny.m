function edge_img = my_canny( img, high_thresh, low_thresh )
%MY_CANNY performs edge detection using the Canny Edge Detector
%   It takes a grayscale image, a high threshold and a low threshold (for
%   double thresholding) and returns a binary image containing the edge
%   points.
    mask = fspecial('gaussian',5,1);
    filtered_img = imfilter(img,mask);
    [grad_mag,grad_dir] = calculate_gradient(filtered_img);
    %mean = mean2(img);
    %std = std2(img);
    %high_thresh = mean+std;
    %low_thresh = mean-std;
    [grad_mag,grad_dir] = imgradient(img);
    grad_dir = discretize_gradient(grad_mag);
    maxima_img = non_maxima_suppress(grad_mag,grad_dir);
    strong_edge = threshold_matrix(maxima_img,high_thresh);
    weak_edge = threshold_matrix(maxima_img,low_thresh);
    edge_img = hysteresis(strong_edge,weak_edge);
    %scale_mask = fspecial('gaussian',5,2); 
    %edge_img = imfilter(edge_img,scale_mask);
    
end



function [lowThresh, highThresh] = selectThresholds(magGrad)

[m,n] = size(magGrad);
counts=imhist(magGrad, 64);
    highThresh = find(cumsum(counts) > .7*m*n,1,'first') / 64;
    highThresh = highThresh*255;
    lowThresh = highThresh*.4;
    
end


function [grad_mag,grad_dir] = calculate_gradient(img)
%CALCULATE_GRADIENT calculates the gradient magnitude and gradient
%direction of an image.

    %Implement this function
    maskx = [-1 0 1;-2 0 2;-1 0 1];
    masky = [-1 -2 -1;0 0 0;1 2 1];
    resX = conv2(double(img), maskx);
    resY = conv2(double(img), masky);
    grad_mag = sqrt(resX.^2 + resY.^2);
    grad_dir = atan(resY/resX);
    
end

function grad_dir = discretize_gradient(grad_angle)
%DISCRETIZE_GRADIENT takes in a matrix containg a set of angles between
%-pi/2 and +pi/2 radians and discretizes them to an integer indication the
%nearest direction in an image where the values correspond to:
%   1 - Horizontal
%   2 - Diagonally upwards-and-right
%   3 - Vertical
%   4 - Diagonally upwards-and-left
    grad_angle = 8*grad_angle/pi;
    grad_dir = zeros(size(grad_angle));
    grad_dir((grad_angle>=-1) & (grad_angle<1)) = 1;
    grad_dir((grad_angle>=1) & (grad_angle<3)) = 2;
    grad_dir((grad_angle<-3) | (grad_angle>=3)) = 3;
    grad_dir((grad_angle>=-3) & (grad_angle<-1)) = 4;
end

function maxima_img = non_maxima_suppress(grad_mag,grad_dir)
%Given a matrix of gradient magnitudes and a matrix of gradient directions
%(as discretized by DISCRETIZE_GRADIENT), NON_MAXIMA_SUPPRESS returns a
%matrix where all values which are non-maximal in their local gradient
%directions are set to 0. Those which are maximal remain unchanged.
    grad_mag_e = expand_matrix(grad_mag);
    dir_1_max = max(grad_mag_e(2:end-1,1:end-2),grad_mag_e(2:end-1,3:end));
    dir_2_max = max(grad_mag_e(1:end-2,3:end),grad_mag_e(3:end,1:end-2));
    dir_3_max = max(grad_mag_e(1:end-2,2:end-1),grad_mag_e(3:end,2:end-1));
    dir_4_max = max(grad_mag_e(1:end-2,1:end-2),grad_mag_e(3:end,3:end));
    
    correct_dir_max = zeros(size(grad_mag));
    correct_dir_max(grad_dir == 1) = dir_1_max(grad_dir ==1);
    correct_dir_max(grad_dir == 2) = dir_2_max(grad_dir ==2);
    correct_dir_max(grad_dir == 3) = dir_3_max(grad_dir ==3);
    correct_dir_max(grad_dir == 4) = dir_4_max(grad_dir ==4);
    
    maxima_img = grad_mag;
    maxima_img(grad_mag<=correct_dir_max) = 0;
    
    function new_mat = expand_matrix(old_mat)
    %EXPAND_MATRIX adds a border of zeros to the original matrix passed to
    %it. It should only be used as a helper function for
    %NON_MAXIMA_SUPPRESS
        new_mat = zeros(size(old_mat,1)+2,size(old_mat,2)+2);
        new_mat(2:end-1,2:end-1) = old_mat;
    end
end

function t_img = threshold_matrix(mat,thresh)
%THRESHOLD_IMAGE takes in a matrix and a threshold. It returns a new matrix
%which is 0 where the original matrix was less than the threshold and 1
%elsewhere.
    
    %Implement this function
    mat(mat<thresh) = 0;
    mat(mat>=thresh) = 1;  
    t_img = mat;
end

function joined_img = hysteresis(strong_edge,weak_edge)
%HYSTERESIS persorms image hysteresis, joining pixels in strong_edge using
%connecting pixels in weak_edge.
    [r,c] = find(strong_edge);
    joined_img = bwselect(weak_edge,c,r,8);
end