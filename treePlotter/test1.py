# _*_coding: utf-8_*_


import math
import numpy as np
from tree import *
from treePlotter import *

DataSet = [[1, 1, 'yes'],
          [1, 1, 'yes'],
          [1, 0, 'no'],
          [0, 1, 'no'],
          [0, 1, 'no']]
labels = ['no surfacing', 'flippers']
def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]

myTree = creatTree(DataSet,labels)
print myTree

createPlot(myTree)
lensesLabels = ['age','prescript','astigmatic', 'tearRate']
fr = open('lenses.txt')


