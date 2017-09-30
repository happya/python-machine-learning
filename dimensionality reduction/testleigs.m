clear all;
clc;
% % Swiss Roll
% N = 1600;
% tt1 = (3*pi/2)*(1+2*rand(1,N));  height = 20*rand(1,N)-10;
% X = [tt1.*cos(tt1); (height); tt1.*sin(tt1)]; 
%% create swiss roll data
N = 1600; % number of points considered
t = rand(1,N);
t = sort(4*pi*sqrt(t))'; 

%t = sort(generateRVFromRand(2^11,@(x)1/32/pi^2*x,@(x)4*pi*sqrt(x)))';
z = 8*pi*rand(N,1); % random heights
x = (t+.1).*cos(t);
y = (t+.1).*sin(t);
X = [x,y,z]'; % data of interest is in the form of a 3-by-N matrix

Y = lle(X,10,2)';
idx = kmeans(Y(:,1),5);
cmaptemp = jet(5);
cmap = jet(N);
for i=1:N
    cmap(i,:)=cmaptemp(idx(i),:);
end
figure,subplot(1,2,1)
scatter3(X(1,:),X(2,:),X(3,:),20,jet(N));
title('Original data');
subplot(1,2,2)
scatter(Y(:,1),Y(:,2)+1,20,cmap)
ylim([-0.1 0.1])
title('LLE embedding')