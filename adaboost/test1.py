


from adaboost import *
import numpy as np



# dataMat, classLabels = loadSimpData()
# classfiers = adaBoostTrainDs(dataMat, classLabels, 9)
# #print adaClassify([[5,5], [0, 0]], classfiers)

dataArr, labelArr = loadDataSet('horseColicTraining2.txt')
classfiers, aggClassEst= adaBoostTrainDs(dataArr, labelArr, 10)
print classfiers
# testDataArr, testLabelArr = loadDataSet('horseColicTest2.txt')
# predLabel = adaClassify(testDataArr, classfiers)
# numOfTest = np.shape(testDataArr)[0]
# error = np.mat(np.ones((numOfTest, 1)))
# totalErr = error[predLabel != np.mat(testLabelArr).T].sum()
# errorRate = float(totalErr)/numOfTest
# print errorRate

# plotROC(aggClassEst.T, labelArr)