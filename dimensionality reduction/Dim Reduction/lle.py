import numpy as np
from scipy.sparse import eye, linalg


def kernel(inX):
    # input data matrix inX: D x N
    # calculate distance matrix, since the exact value is not important, we don't calculate square root
    # return: distance Matrix (N x N)
    D, N = np.shape(inX)
    # Ker[i,j]: <x_i, x_j>
    Ker = inX.T*inX # N x N
    disX = np.mat(np.zeros((N, N)))

    #for i in range(N):
    #   for j in range(N):
    #        disX[i,j] = Ker[i,i] + Ker[j,j] - 2. * Ker[i,j]

    Xii = np.reshape([Ker[i,i] for i in range(N)],(N,1))
    Xii = np.mat(Xii)
    for i in range(N):
        disX[:,i] = Ker[i,i] + Xii - 2.0 * Ker[:,i]
    return disX

def sortDis(disX,k):
    index = np.argsort(disX, axis=0)
    index = np.mat(index)
    neighbors = index[1:k+1,:]
    return neighbors

def findW(inX, neighbors,k):
    D, N = np.shape(inX)
    w = np.mat(np.zeros((k, N)))
    Ni = np.mat([])
    for i in range(N):
        x_i = inX[:,i]
        Xi = np.tile(x_i,(1, k))
        Ni = np.mat(np.zeros((D,k)))
        j = 0
        for index in neighbors[:,i].getA():
            Ni[:,j] = inX[:,index]
            j += 1

        Si = (Xi - Ni).T * (Xi - Ni)
        if k>D:
            tol = 1.0e-3
        else:
            tol = 0
        Si += tol * np.trace(Si) * np.mat(np.eye(k,k))
        invSi = np.linalg.inv(Si)
        d1 = invSi.sum(axis=1)
        d2 = np.sum(d1)
        w[:,i] = d1/d2
    return w

def proj(w,neighbors,d):
    # change w (k x N) to sparse matrix spW (N x N)
    k, N = np.shape(neighbors)
    spW = np.mat(np.zeros((N, N)))
    w = np.mat(w)
    for i in range(N):
        wIdx = 0
        for j in neighbors[:,i].getA():
            spW[j,i] = w[wIdx,i]
            wIdx += 1
    # construct M
    M = (eye(N)-spW)*(eye(N)-spW).T
    # M = (M.T).dot(M).tocsr()


    # obtain Y
    Y = np.mat(np.zeros((d,N)))
    eigval, eigvec = np.linalg.eig(M)
    idx = np.argsort(eigval)
    Y = eigvec[:,idx[1:d+1]]
    return Y






def laplacianEigen(distance, k, d):
    # W: similarity matrix, symmetrix, if two nodes are connected, set as 1; otherwise, set as 0
    # D: degree matrix, define the number of nodes connected
    # L: Laplacian matrix, L = D-W
    index = np.argsort(np.array(distance),axis=0)
    neighbors = index[1:k+1][:]
    W = np.zeros((N,N))
    for i in range(N):
        neighbor = neighbors[:, i] # for node i, find its k-nearest neighbors
        # init W
        W[i, neighbor] = 1
        W[neighbor, i] = 1
    D = np.diag(W.sum(1))
    L = D -W
    eigval, eigvec = linalg.eigs(M)
    idx = np.argsort(eigval)

    return np.mat(vec).T*sqrt(N)

