from lle import *
import numpy as np

import matplotlib.pyplot as plt
from sklearn.cluster import k_means


def loadDataSet(filename):
    file = open(filename)
    dataMat = []
    for line in file.readlines():
        lineList = line.strip().split()

        dataMat.append([float(lineList[0]),float(lineList[1]),float(lineList[2])])
    dataMat = np.mat(dataMat).T
    return dataMat

# generate swiss roll dataset 3 x N
inX = loadDataSet('swissroll.dat')
N = 1600
disX = kernel(inX)
k = 5
neighbors = sortDis(disX,k)
w = findW(inX,neighbors,k)
Y = proj(w,neighbors,2)
Y = (np.mat(Y)).real *np.sqrt(N)
#centroids, clusterAsses = k_means(Y,5)
print(np.shape(Y))
sp = plt.figure(111)
plt.scatter(Y[:,0].getA(), Y[:,1].getA())
#sp.set_title("LLE embedding")
plt.show()

