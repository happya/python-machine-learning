

import matplotlib.pyplot as plt


decisionNode = dict(boxstyle='sawtooth',fc='0.8')
leafNode = dict(boxstyle='round4',fc='0.8')

arrow_args = dict(arrowstyle='<-') # head_length=0.4,head_width=0.2, point to the text





def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    # 'axes fraction': fraction of axes from the lower left
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',\
                           xytext=centerPt,textcoords='axes fraction',\
                           va='center',ha='center', bbox=nodeType, arrowprops=arrow_args)


# def creatPlot():
#     fig = plt.figure(1, facecolor='white')
#     fig.clf()
#     creatPlot.ax1 = plt.subplot(111, frameon=False)
#     plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
#     plotNode('a decision node', (0.5, 0.1), (0.1, 0.8), decisionNode)
#     plt.show()

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]

    for key in secondDict.keys():
        print secondDict[key]
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0; thisDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth+=1
        if thisDepth>maxDepth:
            maxDepth = thisDepth
    return maxDepth

def plotMidText(cntrPt, parentPt, txtString):
    xmid = (parentPt[0]+cntrPt[0])/2.0
    ymid = (parentPt[1]+ cntrPt[1])/2.0+0.05
    createPlot.ax1.text(xmid, ymid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]  # txt label parent node
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)

    plotMidText(cntrPt, parentPt, nodeTxt)
    print plotTree.xOff, cntrPt, parentPt, firstStr
    # plot annotate with arrows point from parentPt to cntrPt
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff -= 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff += 1.0/plotTree.totalW
            print "xOff = %f" %plotTree.xOff
            # plot annotate with arrows point from cntrPt to current (x,y)
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), \
                     cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff += 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    # createPlot.ax1 = plt.subplot(111,frameon=False)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    key1 = inTree.keys()[0]
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()