% LLE ALGORITHM (using K nearest neighbors)

%

% [Y] = lle(X,K,dmax)

%

% X = data as D x N matrix (D = dimensionality, N = # of points)

% K = number of neighbors

% dmax = max embedding dimensionality

% Y = embedding as dmax x N matrix

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [Y] = lleDR(X,K,d)

[D,N] = size(X);

%D x N, D-dimension vector, N-sample points

fprintf(1,'LLE running on %d points in %d dimensions\n',N,D);

% STEP1: COMPUTE PAIRWISE DISTANCES & FIND NEIGHBORS



fprintf(1,'-->Finding %d nearest neighbours.\n',K);

X2 = sum(X.^2,1);

%??X???????2?????????????

%if two point X=(x1,x2),Y=(y1,y2)

%than the distance between X and Y is sqtr((x1-y1)^2+(x2-y2)^2)

distance = repmat(X2,N,1)+repmat(X2',1,N)-2*X'*X;



[sorted,index] = sort(distance);

% sort distance and choose the first K-nearest 
% (the first is discarded since the nearest neighbor is self)

neighborhood = index(2:(1+K),:);

% STEP2: SOLVE FOR RECONSTRUCTION WEIGHTS



fprintf(1,'-->Solving for reconstruction weights.\n');

if(K>D)

fprintf(1,' [note: K>D; regularization will be used]\n');

tol=1e-3; % regularlizer in case constrained fits are ill conditioned

else

tol=0;

end

W = zeros(K,N);

for ii=1:N

% neighborhood(:,ii): the index of K-nearest neighbors of iith point
% X(:,neighborhood(:,ii)): K-nearest neighbors of iith point
% substract the X(:,ii): shift iith point to origin
z = X(:,neighborhood(:,ii))-repmat(X(:,ii),1,K); 


C = z'*z; % local covariance

C = C + eye(K,K)*tol*trace(C); % regularlization (K>D)

W(:,ii) = C\ones(K,1); % solve Cw=1

W(:,ii) = W(:,ii)/sum(W(:,ii)); % enforce sum(w)=1

end;

% STEP 3: COMPUTE EMBEDDING FROM EIGENVECTS OF COST MATRIX M=(I-W)'(I-W)



fprintf(1,'-->Computing embedding.\n');

% M=eye(N,N); use a sparse matrix with storage for 4KN nonzero elements

M = sparse(1:N,1:N,ones(1,N),N,N,4*K*N);

for ii=1:N

% w: the iith colomn of W
w = W(:,ii);

% calculate M = (I-W)(I-W)' = I - W - W.T - W*W' 
% Here W is a N x N matrix with the non-adjacent edge
% weights set to zero, 
% while other edges set to the weight value stored in w.

% jj: the K-nearest neighbors of iith point
jj = neighborhood(:,ii);


M(ii,jj) = M(ii,jj) - w'; 

M(jj,ii) = M(jj,ii) - w;

M(jj,jj) = M(jj,jj) + w*w';

end;

% CALCULATION OF EMBEDDING

options.disp = 0; options.isreal = 1; options.issym = 1;

[Y1,eigenvals] = eigs(M,d+1,0,options);

%[Y,eigenvals] = jdqr(M,d+1);%change in using JQDR func

Y = Y1(:,2:d+1)'*sqrt(N); % bottom evect is [1,1,1,1...] with eval 0

fprintf(1,'Done.\n');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% other possible regularizers for K>D

% C = C + tol*diag(diag(C)); % regularlization

% C = C + eye(K,K)*tol*trace(C)*K; % regularlization