'''
this is a test file for k-means clustering
'''

from __future__ import division
import numpy as np
from kMeans import *


dataMat = loadDataSet('testSet2.txt')


centroids, clusterAsses = kMeans(dataMat, 4, distMeas=distEclud, createCent=randCent)
#centroids, clusterAsses = biKmeans(dataMat, 3, distMeas=distEclud)
# print centroids
fig = plt.figure()
plt.style.use('ggplot')
colors = ['#4EACC5', '#FF9C34', '#4E9A06']
for k in range(3):
# for k, col in zip(range(3), plt.rcParams['axes.color_cycle']):
    X = dataMat[np.nonzero(clusterAsses[:, 0].A == k)[0]]
    plt.scatter(X[:, 0], X[:, 1], s=30, c=colors[k])
    plt.scatter(centroids[k, 0], centroids[k, 1], s=120, c=colors[k], marker='+')
plt.grid(False)
plt.show()