# _*_ coding: utf-8_*_
'''
adaboost: linear superposition of several weak-classifiers to
build a strong-classifiers
'''



import numpy as np
import matplotlib.pyplot as plt

def loadSimpData():
    datMat = np.matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = np.array([1.0, 1.0, -1.0, -1.0, 1.0])
    return datMat, classLabels

def loadDataSet(filename):
    fr = open(filename)
    dataArr = []
    labelArr = []
    for line in fr.readlines():
        lineArr = []
        lineList = line.strip().split('\t')
        numFeat = len(lineList) - 1
        for i in range(numFeat):
            lineArr.append(float(lineList[i]))
        dataArr.append(lineArr)
        labelArr.append(float(lineList[-1]))

    return dataArr, labelArr



def stumpClassify(dataMat, dim, threshVal, threshIneql):
    m = np.shape(dataMat)[0]
    retArr = np.ones((m, 1))

    if threshIneql == 'lt':
        retArr[dataMat[:, dim] <= threshVal] = -1.0

    else:
        retArr[dataMat[:, dim] >= threshVal] = -1.0
    return retArr


# 构建基于单决策树的弱分类器
# 对数据集中的每一个特征，按照一定步长建立单层决策树
def buildStump(dataArr, classLabels, D):
    dataMat = np.mat(dataArr)
    labelMat = np.mat(classLabels).transpose()
    m, n = np.shape(dataMat)
    numSteps = 10
    bestStump = {}
    bestClassPredMat = np.mat(np.zeros((m, 1)))
    minError = np.inf
    for j in range(n):
        minVal = np.min(dataMat[:, j])
        maxVal = np.max(dataMat[:, j])
        stepSize = (maxVal - minVal)/numSteps
        for i in range(-1, int(numSteps) + 1):
            for threshIneql in ['lt', 'gt']:
                threshVal = minVal + float(i) * stepSize
                errArr = np.ones((m, 1))
                predictVals = stumpClassify(dataMat, j, threshVal, threshIneql)
                errArr[predictVals == labelMat] = 0
                weightError = D.T * errArr
                #print "split: dim %d, thresh %.2f, thresh inequl: %s, the weight error is %.3f"\
                #%(j, threshVal, threshIneql, weightError)
                if weightError < minError:
                    minError = weightError
                    bestClassPredMat = predictVals.copy()
                    #print bestClassPredMat
                    bestStump['dim'] = j
                    bestStump['thresh'] = threshVal
                    bestStump['ineql'] = threshIneql
    return bestStump, minError, bestClassPredMat

# 迭代以产生多个弱分类器，并更新权重矩阵D
# 多个弱分类器线性叠加形成新分类器
def adaBoostTrainDs(dataArr, classLabels, numIter):
    numData = np.shape(dataArr)[0]
    D = np.mat(np.ones((numData, 1)))/numData
    aggClassify = np.mat(np.zeros((numData, 1)))
    weakClassifiers = []
    labelMat = np.mat(classLabels)
    for j in range(numIter):
        bestStump, error, bestClassPredMat = buildStump(dataArr, classLabels, D)
        #print bestClassPredMat
        #alpha = 0.5 * np.log((1.0 - error)/max(error, 1e-16))
        alpha = float(0.5 * np.log((1.0 - error) / max(error, 1e-16))) #change alpha from matrix to number
        bestStump['alpha'] = alpha
        weakClassifiers.append(bestStump)
        #print labelMat.T, bestClassPredMat
        expon = np.multiply((-alpha * labelMat).T, bestClassPredMat)
        Zi = np.multiply(D, np.exp(expon))
        Z = np.sum(Zi)
        D = Zi/Z
        # 分类器线性叠加
        aggClassify += alpha * bestClassPredMat
        #print "aggClassify: ", aggClassify.T
        aggErrors = np.multiply(np.sign(aggClassify) != labelMat.T, np.ones((numData, 1)))
        errRate = aggErrors.sum()/numData
        print 'errorate', errRate
        if errRate == 0:
            break
    return weakClassifiers, aggClassify

# 将训练好的分类器用来检测test数据
# 即将多个弱分类器进行线性叠加

def adaClassify(dataArr, weakClassifiers):
    dataMat = np.mat(dataArr)
    m = np.shape(dataMat)[0]
    aggClassifiers = np.mat(np.zeros((m, 1)))
    for i in range(len(weakClassifiers)):
        classEst = stumpClassify(dataMat, weakClassifiers[i]['dim'],\
                                 weakClassifiers[i]['thresh'],\
                                 weakClassifiers[i]['ineql'])
        aggClassifiers += weakClassifiers[i]['alpha'] * classEst
        print aggClassifiers
    return np.sign(aggClassifiers)

def plotROC(predStrengh, classLabels):
    cur = (1.0, 1.0)
    ysum = 0.0
    numPosClas = (np.array(classLabels) == 1.0).sum()
    yStep = 1.0 / numPosClas
    xStep = 1.0 / (len(classLabels) - numPosClas)
    sortedIndex = predStrengh.argsort()
    fig = plt.figure()
    fig.clf()
    ax = fig.add_subplot(111)
    for index in sortedIndex.tolist()[0]:
        if classLabels[index] == 1.0:
            dx = 0
            dy = yStep
        else:
            dx = xStep
            dy = 0
            ysum += cur[1]
        ax.plot([cur[0], cur[0] - dx], [cur[1], cur[1] - dy], c = 'b')
        cur = (cur[0] - dx, cur[1] - dy)
    ax.plot([0, 1], [0, 1], 'b--')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    ax.axis([0, 1, 0, 1])
    plt.show()
    print "the area is: ", ysum * xStep





