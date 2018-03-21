clc;
clear all;

I = imread('girl.png');
R = I(:,:,1);
G = I(:,:,2);
B = I(:,:,3);

h = fspecial('gaussian', 8,8);
blur_R = imfilter(R,h);
blur_G = imfilter(G,h);
blur_B = imfilter(B,h);

blur_I = cat(3,blur_R,blur_G,blur_B);

figure;
% subplot(2,2,1)
% imshow(I)
% title('original')

% subplot(2,2,2)
% imshow(blur_I)
% title('blurred')
edge=I-blur_I;
sharpen1=I+edge;
% 
subplot(2,2,1)
imshow(I)
title('original')
% imshow(edge)
% title('edge')
% subplot(2,2,4)
subplot(2,2,2)
imshow(sharpen1)
title('sharpen-original+edge')

sharpen2=I+edge*3;
subplot(2,2,3)
imshow(sharpen2)
title('sharpen-original+edge*3')
sharpen3=I+edge*6;
subplot(2,2,4)
imshow(sharpen3)
title('sharpen-original+edge*6')