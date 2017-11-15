function [] = display_laplacian_result( img )
%DISPLAY_LAPLACIAN_RESULT Summary of this function goes here
%   Detailed explanation goes here
laplacian = [0,1,0;1,-4,1;0,1,0];
laplacian_img = filter2(laplacian,img);
scaled_laplacian_img = scale_matrix(laplacian_img);
figure,image(scaled_laplacian_img),axis off,colormap gray(256),title('scaled laplacian img');
figure,image(laplacian_img),axis off,colormap gray(256),title('laplacian img');
figure,image(img),axis off,colormap gray(256),title('original');

end

