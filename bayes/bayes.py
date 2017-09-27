'''
bayes

@ author yyi
'''

import numpy as np
import re
import operator

# creat a list of non-duplicated words exist in the text
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

# set-of-words model: whether the word exist or not
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word %s is not in my vocabulary" % word
    return returnVec

# bag-of-words model: how many times a certain word appears
def bagOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print "the word %s is not in my vocabulary" % word
    return returnVec

# trainMatrix: consist of vector from each text file
# count the probability of each word
def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = (np.sum(trainCategory))/float(numTrainDocs)
    p0Num = np.ones(numWords)
    p1Num = np.ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += np.sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += np.sum(trainMatrix[i])
    p1Vec = np.log(p1Num/p1Denom)
    p0Vec = np.log(p0Num/p0Denom)


    return p1Vec, p0Vec, pAbusive

def classifyNB(vec2Classify, p1Vec, p0Vec, pClass1):
    p1 = np.sum(vec2Classify * p1Vec) + np.log(pClass1)
    p0 = np.sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)
    if p1>p0:
        return 1
    else:
        return 0

def textParse(bigString):
    listOfTokens = re.split(r'\W*', bigString)
    return [token.lower() for token in listOfTokens if len(token) > 2]

def spamTest():
    docList = []
    fullText = []
    classList = []
    for i in range(1, 26):
        wordList = textParse(open('spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)

        wordList = textParse(open('ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainSet = range(50)
    testSet = []
    for i in range(10):
        randIdx = int(np.random.uniform(0, len(trainSet)))
        testSet.append(trainSet[randIdx])
        del(trainSet[randIdx])
    trainMat = []
    trainClasses = []
    for docIndex in trainSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p1Vec, p0Vec, pSpam = trainNB0(np.array(trainMat), np.array(trainClasses))
    errorCount = 0

    for docIndex in testSet:
        wordVec = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(np.array(wordVec), p1Vec, p0Vec, pSpam) != classList[docIndex]:
            errorCount += 1
            print 'classification error', docList[docIndex]
    print "the error rate is ", float(errorCount)/len(testSet)
    return float(errorCount)/len(testSet)

def calcMostFreq(vocabList, fullText):
    freqDict = {}
    for word in vocabList:
        freqDict[word] = fullText.count(word)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1),\
                        reverse=True)
    return sortedFreq[:100]

def localWords(feed1, feed0):
    docList = []
    fullText = []
    classList = []
    minLen = min(len(feed1['entries']), feed0['entries'])
    print minLen

    # each time visit a RSS feed
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)

        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)


    vocabList = createVocabList(docList)
    top100Words = calcMostFreq(vocabList, fullText)

    # remove high frequency words
    for word in top100Words:
        if word[0] in vocabList:
            vocabList.remove(word[0])


    trainSet = range(2*minLen)
    testSet = []
    for i in range(20):
        randIndex = int(np.random.uniform(0, len(trainSet)))
        testSet.append(trainSet[randIndex])
        del(trainSet[randIndex])

    trainMat = []
    trainClasses = []
    for docIndex in trainSet:
        trainMat.append(bagOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])

    p1Vec, p0Vec, pSpam = trainNB0(np.array(trainMat), np.array(trainClasses))

    errorCount = 0.0
    for docIndex in testSet:
        wordVec = bagOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(np.array(wordVec), p1Vec, p0Vec, pSpam) != classList[docIndex]:
            errorCount += 1.0

    print "the error rate is: ", errorCount/len(testSet)
    return vocabList, p1Vec, p0Vec

def getTopWords(ny, sf):
    volcabList, p1V, p0V = localWords(sf, ny)
    topSF = []
    topNY = []
    for i in range(len(p1V)):
        if p1V[i] > -4.5:
            topSF.append((volcabList[i], p1V[i]))
        if p0V[i] > -4.5:
            topNY.append((volcabList[i], p0V[i]))
    # topSF, topNY are tuples
    # the first values are high-freq words,
    # the second values are corresponding probability
    # the sort function sort these words with probability from highest to lowest
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)

    print 'NY '*20

    for item in sortedNY:
        print item[0], item [1]

    print 'SF '*20
    for item in sortedSF:
        print item[0], item[1]




