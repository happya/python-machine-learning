# _*_ coding: utf-8 _*_



from knn import *
import numpy as np
from os import listdir
from matplotlib import pyplot as plt
from matplotlib import font_manager
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号



# fr=open('0_0.txt')
# img0 = np.mat(np.zeros((32,32)))
# i=0
# for line in fr.readlines():
#     for j in range(32):
#         print line[j]
#         img0[i,j]= int(line[j])
#     i+=1
#
# fig=plt.figure()
# ax=fig.add_subplot(111)
# ax.imshow(img0, cmap='gray')
# plt.show()

# filelist = listdir('trainingDigits')
# print filelist[1]
handwritingClassTest()