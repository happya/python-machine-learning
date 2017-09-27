# _*_ coding: utf-8 _*_



from knn import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

hoRatio = raw_input("please input the value (between 0 to 1):\n")
dataMat,datinglabels=loadDataSet('datingTestSet2.txt')
normData= autoNorm(dataMat)[0]
m,n = np.shape(normData)

numTestVecs = int(m*float(hoRatio))
errorCount = 0
dataTra = normData[numTestVecs:m]
labelTra = datinglabels[numTestVecs:m]
for i in range(numTestVecs):
    classifierResult = classify0(normData[i,:],dataTra, labelTra,k=3)

    print "%d times: the classifier return: %d, the real label is : %d"\
    % (i,classifierResult, datinglabels[i])
    if (classifierResult != datinglabels[i]):
        errorCount+=1

print ("the error rate is : %.2f %%" %(errorCount*100/float(numTestVecs)))

# clarifyPerson()
