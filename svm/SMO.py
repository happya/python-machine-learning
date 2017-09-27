import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

def loadDataSet(filename):
    dataMat=[]; labelMat=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m):
    j=i
    while(j==i):
        j=int(np.random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj>H:
        aj=H
    if aj<L:
        aj=L
    return aj



def smoSimple(dataMatIn,classLabels,C,toler,maxIter):
    dataMatrix=np.mat(dataMatIn)
    labelMat = np.mat(classLabels).transpose()
    b=0
    m,n = np.shape(dataMatrix)
    alphas=np.zeros((m,1))
    alphas=np.mat(alphas)
    iter=0
    while(iter<maxIter):
        alphaPairsChanged=0

        ### fXi is the anticipated classfication value
        ### Ei is the errorness
        ### is fXi against KKT (yiEi) and alpha not at the boundary
        ### use SMO algo to update new alpha
        ##############################################
        for i in range(m):
            fXi=float(np.multiply(alphas,labelMat).T*\
                      (dataMatrix*dataMatrix[i,:].T))+b
            Ei=fXi-float(labelMat[i])
            yiEi=float(labelMat[i])*Ei
            if ((yiEi<-toler) and (alphas[i]<C)) or \
                    ((yiEi>toler) and (alphas[i]>0)):
                j=selectJrand(i,m)
                fXj=float(np.multiply(alphas,labelMat).T*\
                      (dataMatrix*dataMatrix[j,:].T))+b
                Ej=fXj-float(labelMat[j])
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                ###########
                ### define the boundary of alpha
                ################################
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j]-alphas[i])
                    H = min(C, C+alphas[j]-alphas[i])
                else:
                    L = max(0, alphas[i]+alphas[j]-C)
                    H = min(C, alphas[i]+alphas[j])
                if L==H: print "L==H"; continue;

                eta = dataMatrix[i,:] * dataMatrix[i,:].T+ \
                      dataMatrix[j,:] * dataMatrix[j, :].T- \
                      2*dataMatrix[i, :] * dataMatrix[j, :].T
                if eta<=0: print "eta<=0!"; continue

                #######
                ### updata alpha[j]
                alphas[j]+=labelMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)

                if (abs(alphas[j]-alphaJold)<0.0001):
                    print "j not moving large enough"; continue

                ### update alphas[i]
                alphas[i]-= labelMat[i]*labelMat[j]*(alphas[j]-alphaJold)
                ### update b
                b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*\
                        dataMatrix[i,:]*dataMatrix[i,:].T-\
                    labelMat[j]*(alphas[j]-alphaJold)*\
                    dataMatrix[j,:]*dataMatrix[i,:].T
                b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*\
                        dataMatrix[i,:]*dataMatrix[j,:].T-\
                    labelMat[j]*(alphas[j]-alphaJold)*\
                    dataMatrix[j,:]*dataMatrix[j,:].T
                if (0<alphas[i]) and (alphas[i]<C): b=b1
                elif (0<alphas[j]) and (alphas[j]<C): b=b2
                else: b=(b1+b2)/2.0

                ### update times that alphas are changed
                alphaPairsChanged+=1

                print "iter: %d i : %d, pairs changed %d" %\
                      (iter, i, alphaPairsChanged)

        if (alphaPairsChanged==0): iter+=1
        else: iter=0
        print "iteration number: %d: " % iter

    return b, alphas




if __name__ == "__main__":
    dataArr,labelArr=loadDataSet('testSet.txt')
    b, alphas = smoSimple(dataArr,labelArr,0.6, 0.001,40)
    print "b= %f" %b
    labelMat=np.mat(labelArr).transpose()
    dataMat=np.mat(dataArr)
    #print np.shape(alphas),np.shape(np.multiply(alphas,labelMat).T)
    wArr=(np.multiply(alphas,labelMat).T*dataMat).A

    w1=wArr[0][0]
    w2=wArr[0][1]

    w=-w1/w2

    bnor=-b/w2
    r=1/w2
    xrr=np.arange(0,9)
    lp_x2=xrr*w+bnor
    lp_x2up=lp_x2+r
    lp_x2down=lp_x2-r
    print wArr,w,bnor

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataMat[:,0],dataMat[:,1],color='g')
    ax.plot(xrr,lp_x2.T,'b')
    ax.plot(xrr,lp_x2up.T,'b--')
    ax.plot(xrr,lp_x2down.T,'b--')
    plt.show()
