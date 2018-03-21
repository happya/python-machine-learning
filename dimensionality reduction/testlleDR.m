clear all
clc

N = 1600; % number of points considered
t = rand(1,N);
t = sort(4*pi*sqrt(t))';

% Swill roll data
z = 8*pi*rand(N,1); % random heights
x = (t+.1).*cos(t);
y = (t+.1).*sin(t);
X = [x,y,z]'; % data of interest is in the form of a 3-by-N matrix


d = 2
figure
for k = 5:20
    
 Y = lleDR(X,k,d)';
 subplot(4,4,k-4);
 scatter(Y(:,1),Y(:,2)+1,20,jet(N));
 title(['k=',num2str(k)]);
 hold on
end

figure
scatter3(X(1,:),X(2,:),X(3,:),20,jet(N));
title('Original data');
% subplot(1,2,2)
% scatter(Y(:,1),Y(:,2)+1,20,jet(N))