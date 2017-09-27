# _*_ coding: utf-8 _*_


import operator
from os import listdir
import numpy as np
import matplotlib.pyplot as plt



def loadDataSet(filename):
    returnMat=[]
    labelVec=[]
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        returnMat.append([float(lineArr[0]),float(lineArr[1]),float(lineArr[2])])
        labelVec.append(int(lineArr[-1]))
    returnMat = np.array(returnMat)
    # labelVec=np.mat(labelVec).transpose()
    return returnMat, labelVec

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals

    m,n = np.shape(dataSet)
    normDataset = np.mat(np.zeros((m,n)))
    normDataset = dataSet-np.tile(minVals,(m,1))
    normDataset = normDataset/np.tile(ranges,(m,1))

    return normDataset, ranges, minVals

def classify0(inX, dataSet, labels,k):
    # inX: input vector
    # dataSet: training data set
    # labels： label vector
    # k: k-nearest labors

    m,n = np.shape(dataSet)
    diffMat = np.tile(inX,(m,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(1)
    distances = sqDistances**0.5
    sortedDistInd = np.argsort(distances)
    classCount = {}

    # k-nearest neighbor
    for i in range(k):
        # vote for the label of the k-nearest points
        voteIlabel = labels[sortedDistInd[i]]
        # print voteIlabel
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1

    # sort from the highest scores
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1),\
                              reverse=True)

    return sortedClassCount[0][0]


def clarifyPerson():
    resultsList = ['not at all','in small doses','in large doses']
    percentTat = float(raw_input("percentage of time playing video games every week:"))
    ffMiles = float(raw_input("flight miles earned every year: "))
    iceCreams = float(raw_input("liters of ice creams consumed every week: "))
    datingMat, labelVec = loadDataSet("datingTestSet2.txt")
    normDat, ranges, minVals = autoNorm(datingMat)
    inX = np.array([ffMiles, percentTat, iceCreams])
    norinX = (inX-minVals)/ranges
    classifyResult = classify0(norinX,normDat,labelVec,3)
    print "you will probably like this person : ", resultsList[classifyResult-1]


# convert a 32*32 image to a (1*1024) array
def img2vector(filename):
    returnVect = np.zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(line[j])
    return returnVect

def handwritingClassTest():
    hwlabels = []
    trainingFileList = listdir('trainingDigits')
    testFileList = listdir('testDigits')
    m = len(trainingFileList); mTest = len(testFileList)
    trainingMat = np.zeros((m,1024))
    for i in range(m):
        fileName = trainingFileList[i]
        fileStr = fileName.split('.')[0]
        classNameStr = int(fileName.split('_')[0])
        hwlabels.append(classNameStr)
        trainingMat[i, :] = img2vector('trainingDigits/%s'%fileName)

    errorCount = 0.0

    for i in range(mTest):
        fileName = testFileList[i]
        fileStr = fileName.split('.')[0]
        classNameStr = int(fileName.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s'%fileName)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwlabels,3)

        print "the classifier returns: %d, the real answer is: %d"\
        %(classifierResult, classNameStr)
        if (classifierResult != classNameStr):
            errorCount+=1
    print "\nthe total error number is: %d" %errorCount
    print "\nthe total error rate is %f" % (errorCount/float(mTest))













