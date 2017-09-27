'''
k-means clustering
'''

import numpy as np
import matplotlib.pyplot as plt
import math

def loadDataSet(filename):
    file = open(filename)
    dataList = []
    for line in file.readlines():
        lineList = line.strip().split('\t')
        fltline = map(float, lineList)
        dataList.append(fltline)
    dataMat = np.mat(dataList)
    return dataMat

def distEclud(vecA, vecB):
    diff = vecA - vecB
    diffSum = np.sum(np.power(diff, 2))
    return np.sqrt(diffSum)

def randCent(dataMat, k):
    n = np.shape(dataMat)[1]
    centroids = np.mat(np.zeros((k, n)))
    for j in range(n):
        minJ = np.min(dataMat[:, j])
        maxJ = np.max(dataMat[:, j])
        rangeJ = float((maxJ - minJ))
        centroids[:, j] = np.mat(minJ + rangeJ * np.random.rand(k, 1))
    return centroids

def kMeans(dataMat, k, distMeas = distEclud, createCent = randCent):
    m = np.shape(dataMat)[0]
    centroids = createCent(dataMat, k)
    clusterChanged = True
    clusterAsses = np.mat(np.zeros((m, 2)))
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            mindist = np.inf
            minIndex = -1
            for j in range(k):
                dist = distMeas(dataMat[i, :], centroids[j, :])
                if dist < mindist:
                    mindist = dist
                    minIndex = j
            if clusterAsses[i, 0] != minIndex:
                clusterChanged = True
            clusterAsses[i, :] = minIndex, mindist ** 2
        for cent in range(k):
            pointsInClus = dataMat[np.nonzero(clusterAsses[:, 0].A == cent)[0]]
            centroids[cent, :] = pointsInClus.mean(axis=0)
    return centroids, clusterAsses


def biKmeans(dataMat, k, distMeas=distEclud):
    m = np.shape(dataMat)[0]
    clusterAsses = np.mat(np.zeros((m, 2)))

    centroid0 = dataMat.mean(axis=0).tolist()[0]
    for j in range(m):
        dist = distMeas(np.mat(centroid0), dataMat[j, :])
        clusterAsses[j, 1] = dist ** 2
    centList = [centroid0]
    while (len(centList)<k):
        lowestSSE = np.inf
        for i in range(len(centList)):
            # pick out the data points in ith cluster
            pointsInClus = dataMat[np.nonzero(clusterAsses[:, 0].A == i)[0]]

            # employ the kMeans method with k=2 to divide the current cluster
            # to 2 clusters
            centroids, splitClusterAss = kMeans(pointsInClus, 2)
            sseSplit = splitClusterAss[:, 1].sum()
            sseNotSplit = clusterAsses[np.nonzero(clusterAsses[:, 0].A != i)[0], 1].sum()
            if (sseNotSplit + sseSplit) < lowestSSE:
                lowestSSE = sseSplit + sseNotSplit
                bestNewCent = centroids
                bestClasAss = splitClusterAss.copy()
                bestCentToSplit = i

        # after traverse all the existed cluster and evaluated the splitting performance
        # update the cluster splitting results

        # update centroid list
        # very important: must updated after the "bestClasAss" terms
        centList[bestCentToSplit] = bestNewCent[0, :].tolist()[0]
        centList.append(bestNewCent[1, :].tolist()[0])

        # update the cluster Assesement results for the splitting cluster
        # !!! very important: must update the len(cenList) term first


        bestClasAss[np.nonzero(bestClasAss[:, 0].A == 1)[0], 0] = len(centList)-1
        bestClasAss[np.nonzero(bestClasAss[:, 0].A == 0)[0], 0] = bestCentToSplit


        # update the total assessment results, since the number of clusters increases with 1
        # and the indices of the splitting cluster are also updated
        clusterAsses[np.nonzero(clusterAsses[:, 0].A == bestCentToSplit)[0], :] = bestClasAss


        #print "the bestCent to split is : ", bestCentToSplit
    centMat = np.mat(centList)
    # print centMat, clusterAsses
    return centMat, clusterAsses








