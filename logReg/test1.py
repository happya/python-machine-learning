

from logReg import *
import matplotlib.pyplot as plt

dataMat, labelMat = loadDataSet('testSet.txt')
maxIter = 100
weights, w0, w1, w2 = stocGradAscent1(np.array(dataMat), labelMat, maxIter)

# num = 100 * maxIter
# times = np.arange(num)
# print np.shape(times), np.shape(w0)
# plotBestFit(weights)
# fig = plt.figure()
# ax1 = fig.add_subplot(311)
# plt.plot(times, np.array(w0))
# ax2 = fig.add_subplot(312)
# plt.plot(times, np.array(w1))
# ax3 = fig.add_subplot(313)
# plt.plot(times, np.array(w2))
# plt.show()

colicTest()
multiTest(10)