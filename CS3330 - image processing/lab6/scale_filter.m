img = scale_matrix(f);
mask = fspecial('average',3);
filtered_img = filter2(mask,img);
figure,image(filtered_img),axis off,colormap gray(256);