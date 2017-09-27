from smoPlatt import *
import numpy as np




dataArr,labelArr=loadDataSet('testSetRBF.txt')
k1=raw_input("please input the value of sigma:\n")
k1=float(k1)
kTup=('rbf',k1)
b,alphas=smoPlatt(dataArr,labelArr,200,0.0001,10000,kTup)
datMat=np.mat(dataArr);labelMat=np.mat(labelArr).transpose()
svInd=np.nonzero(alphas.A>0)[0]
sVs=datMat[svInd]
labelSV=labelMat[svInd]

print "there are %d support vectors" %np.shape(sVs)[0]

m,n=np.shape(datMat)

errorCount = 0
for i in range(m):
    kernelEval = kernelTrans(sVs,datMat[i,:],kTup)
    predict=kernelEval.T*np.multiply(labelSV,alphas[svInd])+b
    if np.sign(predict)!=np.sign(labelArr[i]):
        errorCount+=1

print "the training error is: %f" % (float(errorCount)/m)

dataArr,labelArr=loadDataSet('testSetRBF2.txt')
errorCount=0
dataMat=np.mat(dataArr)
labelMat=np.mat(labelArr).transpose()
m,n=np.shape(datMat)

for i in range(m):
    kernelEval = kernelTrans(sVs,datMat[i,:],kTup)
    predict=kernelEval.T*np.multiply(labelSV,alphas[svInd])+b
    if np.sign(predict)!=np.sign(labelArr[i]):
        errorCount+=1

print "the test error is: %f" % (float(errorCount)/m)
