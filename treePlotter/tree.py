# _*_coding: utf-8_*_


import math
import operator
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCount = {}
    for featVec in dataSet:
        currentlabel = featVec[-1]
        labelCount[currentlabel] = labelCount.get(currentlabel,0)+1
    ShannonEnt = 0
    for key in labelCount:
        prob = float(labelCount[key])/numEntries
        ShannonEnt += -prob * math.log(prob, 2)
    return ShannonEnt

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1
    m = len(dataSet)
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0; infoGain = 0
        for value in uniqueVals:
            subList = splitDataSet(dataSet, i, value)
            prob = len(subList)/float(m)
            newEntropy += prob*calcShannonEnt(subList)
        infoGain = -newEntropy + baseEntropy

        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorCnt(classList):
    classCount = {}
    for vote in classList:
        classCount[vote] = classCount.get(vote,0)+1
    sortedClassCount = sorted(classCount.iteritems(),\
                              key=operator.itemgetter(1),reverse=True)
    return classCount[0][0]


def creatTree(dataSet, labels):
    # get the feature list
    classList = [example[-1] for example in dataSet]
    # stop splitting when all the classes are the same
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # stop splitting when there are no more features in the dataset
    # only dataset[-1] exist,like 'yes' or 'no'
    if len(dataSet[0]) == 1:
        return majorCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        sublabels = labels[:]
        myTree[bestFeatLabel][value] = creatTree(splitDataSet(dataSet, bestFeat,value),sublabels)
    return myTree