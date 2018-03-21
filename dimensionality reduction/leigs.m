% Laplacian Eigenmap ALGORITHM (using K nearest neighbors)
%
% [Y] = le(X,K,dmax)
%
% X = data as D x N matrix (D = dimensionality, N = #points)
% K = number of neighbors
% dmax = max embedding dimensionality
% Y = embedding as dmax x N matrix
% Swiss Roll
% tt1 = (3*pi/2)*(1+2*rand(1,N));  height = 20*rand(1,N)-10;
% X = [tt1.*cos(tt1); (height); tt1.*sin(tt1)]; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
function [Y] = leigs(X,K,d)
 
[D,N] = size(X);
fprintf(1,'LE running on %d points in %d dimensions\n',N,D);
 
 
% STEP1: COMPUTE PAIRWISE DISTANCES & FIND NEIGHBORS 
fprintf(1,'-->Finding %d nearest neighbours.\n',K);
 
X2 = sum(X.^2,1);
distance = repmat(X2,N,1)+repmat(X2',1,N)-2*X'*X;
 
[sorted,index] = sort(distance);
neighborhood = index(2:(1+K),:);
% for each colomn j in "neighborhood",it contains the K-nearest neighbors of point j.
% neighborhood:K x N
 
 
 
% STEP2: Construct similarity matrix W
fprintf(1,'-->Constructing similarity matrix.\n');
 
W = zeros(N, N);
% W is symmetric, similarity matrix
for ii=1:N
    W(ii, neighborhood(:, ii)) = 1;
    W(neighborhood(:, ii), ii) = 1;
end
 
% STEP 3: COMPUTE EMBEDDING FROM EIGENVECTS OF L
fprintf(1,'-->Computing embedding.\n');

% D is the degree of graph, so it's diagonal matric, D[i,i] is the value
% that the number of edges connected with node i 
D = diag(sum(W));
L = D-W;
 
% CALCULATION OF EMBEDDING
options.disp = 0; options.isreal = 1; options.issym = 1; 
[Y,eigenvals] = eigs(L,d+1,0,options); % return (d+1) largest eigenvalues and corresponding vectors

% Normalized, discard the first largest ones
Y = Y(:,2:d+1)'*sqrt(N); % bottom evect is [1,1,1,1...] with eval 0
 
 
fprintf(1,'Done.\n');
 
%%%%%%%%%%%%%%%%%%%