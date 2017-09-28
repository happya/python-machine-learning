import numpy as np
from KMeans import *

def distance(inX):
    # input data matrix inX: D x N
    # calculate distance matrix, since the exact value is not important, we don't calculate square root
    # return: distance Matrix (N xN)
    D, N = np.shape(inX)
    inX2 = np.array(inX.sum(1))**2
    distance = np.tile(inX2, (N, 1)) + np.tile(inX2.T, (1, N)) -2.*np.mat(inX2.T)*np.mat(inX2)
    return np.mat(distance)

def laplacianEigen(distance, k, d):
    # W: similarity matrix, symmetrix, if two nodes are connected, set as 1; otherwise, set as 0
    # D: degree matrix, define the number of nodes connected
    # L: Laplacian matrix, L = D-W
    index = np.argsort(np.array(distance),axis=0)
    neighbors = index[1:k+1, :]
    W = np.zeros((N,N))
    for i in range(N):
        neighbor = neighbors[:, i] # for node i, find its k-nearest neighbors
        # init W
        W[i, neighbor] = 1
        W[neighbor, i] = 1
    D = np.diag(W.sum(1))
    L = D -W
    eigs, eigvec = np.linalg(L)
    idx = np.argsort(eigs)
    vec = eigvec[:, -1-d:-1]
    return np.mat(vec).T*sqrt(N)

