# _*_ coding: utf-8 _*_
'''
 created on 20th Oct, 2016
@ author yyi
'''

import numpy as np
import re
import operator
import matplotlib.pyplot as plt


def loadDataSet(filename):
    dataMat = []
    labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat

def sigmoid(z):
    return 1.0/(1 + np.exp(-z))


def gradAssent(dataMatIn, label):
    dataMatrix = np.mat(dataMatIn)
    labelMat = np.mat(label).transpose()
    m, n = np.shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = np.ones((n, 1))
    for i in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = labelMat - h
        weights += alpha * dataMatrix.transpose() * error
    return weights

# 梯度上升算法
# 预测函数h and 预测误差 error are both vectors
# 采取矩阵运算
def plotBestFit(w):
    dataList, labelList = loadDataSet('testSet.txt')
    dataArr = np.array(dataList)
    m, n = np.shape(dataArr)

    # since we regard the dataSet as a vector with each element to be 2-dimensional
    # here x and y are the coordinates in a 2d space
    x1cord = []
    x2cord = []
    y1cord = []
    y2cord = []
    for i in range(m):
        if int(labelList[i]) == 1:
            x1cord.append(dataArr[i, 1])
            y1cord.append(dataArr[i, 2])
        else:
            x2cord.append(dataArr[i, 1])
            y2cord.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x1cord, y1cord, s=30, c='red', marker='o')
    ax.scatter(x2cord, y2cord, s=30, c='green', marker='o')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (- w[0] - w[1] * x)/w[2]  # z = 0
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


# 随机梯度上升算法
# h and error are both numbers
def stocGradAscent0(dataArr, classLabels):
    m, n = np.shape(dataArr)
    step = 0.01
    weights = np.ones(n) # the shape is (n,)
    # 向量乘法是元素运算，与矩阵乘法不同
    for i in range(m):
        h = sigmoid(np.sum(dataArr[i]) * weights)
        error = classLabels[i] - h
        # update weights
        weights += step * error * dataArr[i]
    return weights

def stocGradAscent1(dataArr, classLabels, maxIter=150):
    m, n = np.shape(dataArr)
    weights = np.ones(n)
    w0 = []
    w1 = []
    w2 = []
    for j in range(maxIter):
        dataIndex = range(m)

        for i in range(m):
            step = 0.01 + 4.0/(1.0+j+i)
            randIndex = int(np.random.uniform(0,len(dataIndex)))
            h = sigmoid(np.sum(dataArr[randIndex] * weights))
            error = classLabels[randIndex] - h
            weights += step * error * dataArr[randIndex]
            del(dataIndex[randIndex])
            w0.append(weights[0])
            w1.append(weights[1])
            w2.append(weights[2])
    return weights, w0, w1, w2

def classifyVec(featVec, w):
    prob = sigmoid(np.sum(featVec * w))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0

def colicTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainingSet = []
    trainingLabels = []

    for line in frTrain.readlines():
        lineArr = []
        lineCur = line.strip().split('\t')
        featNum = len(lineCur)-1
        for i in range(featNum):
            lineArr.append(float(lineCur[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(lineCur[-1]))

    trainingWeights = stocGradAscent1(np.array(trainingSet), trainingLabels, 500)[0]
    errorCount = 0.0
    numOfTest = 0.0
    for line in frTest.readlines():
        numOfTest += 1.0
        lineCur = line.strip().split('\t')
        lineArr = []
        featNum = len(lineCur)-1
        for i in range(featNum):
            lineArr.append(float(lineCur[i]))
        if int(classifyVec(np.array(lineArr), trainingWeights)) !=\
            int(lineCur[-1]):
            errorCount += 1.0
    errorRate = errorCount/numOfTest
    print "the errorrate is: ", errorRate

    return errorRate

def multiTest(numTest):
    errorSum = 0.0
    for i in range(int(numTest)):
        errorSum += colicTest()
    print "after %d times of iteration the error rate is %f"\
    % (numTest, errorSum/numTest)





