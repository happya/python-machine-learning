# _*_ coding: utf-8 _*_



from knn import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号



dataMat,datinglabels=loadDataSet('datingTestSet2.txt')


type1In,type2In,type3In = np.nonzero(datinglabels.A==1)[0],\
                          np.nonzero(datinglabels.A==2)[0],\
                          np.nonzero(datinglabels.A==3)[0]
type1, type2, type3 = dataMat[type1In], dataMat[type2In], dataMat[type3In]

fig1 = plt.figure()
axes = fig1.add_subplot(111)
type1Plt, type2Plt, type3Plt = axes.scatter(type1[:, 0],type1[:, 1], s=20,c='red'),\
    axes.scatter(type2[:, 0],type2[:, 1],s=40, c='cyan'), axes.scatter(type3[:, 0], type3[:, 1],s=50, c='green')

plt.xlabel(u'每年飞行的里程数')
plt.ylabel(u'玩视频游戏所耗时间百分比')
axes.legend((type1Plt,type2Plt,type3Plt),(u'看着想吐',u'麻麻得', u'魅力.李佩佩'))
plt.show()
