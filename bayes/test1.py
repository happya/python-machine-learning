'''
 a test file for naive bayes

 @author yyi
'''

import numpy as np
import  matplotlib.pyplot as plt
import re
import feedparser
from bayes import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

listPosts, listClasses = loadDataSet()
myVolcabList = createVocabList(listPosts)
trainMat = []
print len(listClasses)
for postinDoc in listPosts:
    trainMat.append(setOfWords2Vec(myVolcabList,postinDoc))
p1Vec, p0Vec, pAbusive = trainNB0(trainMat,listClasses)
print pAbusive, '\n', p0Vec, len(p1Vec)
print np.sum(p0Vec)
# testEntry = ['love','affection','dog']
# testVec = np.array(setOfWords2Vec(myVolcabList,testEntry))
# print classifyNB(testVec, p1Vec, p0Vec, pAbusive)
totalError = 0.0
# for i in range (50):
#     totalError += spamTest()

print totalError/float(50)
