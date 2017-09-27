

import numpy as np
import matplotlib.pyplot as plt
from SMO import *



def kernelTrans(X,A,kTup):
    # X is the data matrix
    # A is the coordinate of data

    m,n=np.shape(X)
    K=np.mat(np.zeros((m,1)))

    # linear kernel function
    # calculate the inner product between every data pair
    if kTup[0]=='lin': K=X*A.T
    elif kTup[0]=='rbf':
        for j in range(m):
            # X[j,:] is the jth data in the data set
            deltaRow=X[j,:]-A
            # K[j] is the distantce between the jth data to A
            K[j]=deltaRow*deltaRow.T
        K=np.exp(K/(-1*kTup[1]**2))
    else:
        raise NameError("That kernel is not recognized!!!")
    return K


class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler,kTup):
        self.X = dataMatIn
        self.labelMat=classLabels
        self.C=C
        self.tol=toler
        self.m=np.shape(dataMatIn)[0]
        self.alphas=np.mat(np.zeros((self.m,1)))
        self.b=0

        ### first column of eCache is the valid flag
        ### here valid means the Ek has already been calculated
        ### second column of eCache is Ek
        self.eCache=np.mat(np.zeros((self.m,2)))
        self.K=np.mat(np.zeros((self.m,self.m)))
        for i in range(self.m):
            self.K[:,i] = kernelTrans(self.X,self.X[i,:],kTup)




def calcEk(oS, k):
    fXk = float(np.multiply(oS.alphas, oS.labelMat).T *oS.K[:,k] + oS.b)
    Ek = fXk - float(oS.labelMat[k])
    return Ek

def selectJ(i,oS,Ei):
    maxDeltaE=0
    Ej=0
    maxK=-1
    oS.eCache[i]=[1,Ei]
    validEcacheList=np.nonzero(oS.eCache[:,0].A)[0]
    if (len(validEcacheList)>1):
        for k in validEcacheList:
            if k==i: continue
            Ek=calcEk(oS,k)
            deltaE=abs(Ei-Ek)
            if (deltaE>maxDeltaE):
                maxDeltaE=deltaE
                Ej=Ek
                maxK=k
        return maxK,Ej
    else:
        j=selectJrand(i,oS.m)
        Ej=calcEk(oS,j)
    return j,Ej

def updateEk(oS,k):
    Ek=calcEk(oS,k)
    oS.eCache[k]=[1,Ek]

def innerL(i,oS):
    Ei=calcEk(oS,i)
    agKKT=oS.labelMat[i]*Ei
    if ((agKKT<-oS.tol) and (oS.alphas[i]<oS.C)) or\
            ((agKKT>oS.tol) and (oS.alphas[i]>0)):
        j,Ej=selectJ(i,oS,Ei)

        # keep the old value of alphai,alphaj
        alphaIold=oS.alphas[i].copy()
        alphaJold=oS.alphas[j].copy()

        # set the upperest and lowerest boundary of Ej
        if (oS.labelMat[i]!=oS.labelMat[j]):
            L=max(0,oS.alphas[j]-oS.alphas[i])
            H=min(oS.C,oS.alphas[j]-oS.alphas[i]+oS.C)
        else:
            L=max(0,oS.alphas[i]+oS.alphas[j]-oS.C)
            H=min(oS.C,oS.alphas[i]+oS.alphas[j])

        if L==H:
            #print "L==H"
            return 0

        eta=oS.K[i,i]+oS.K[j,j]-2.0*oS.K[i,j]

        if eta<=0:print "eta<=0"; return 0

        oS.alphas[j]+=oS.labelMat[j]*(Ei-Ej)/eta
        oS.alphas[j]=clipAlpha(oS.alphas[j],H,L)

        # update errorness cache of j
        updateEk(oS,j)
        if (abs(oS.alphas[j]-alphaJold)<0.0001):
            # print "j not moving enough"
            return 0
        oS.alphas[i]-=oS.labelMat[i]*oS.labelMat[j]*(oS.alphas[j]-alphaJold)

        # update errorness cache of i
        updateEk(oS,i)

        # update b
        b1=oS.b-Ei-oS.labelMat[i]*oS.K[i,i]*(oS.alphas[i]-alphaIold)-\
            oS.labelMat[j]*oS.K[i,j]*(oS.alphas[j]-alphaJold)
        b2 =oS.b-Ej - oS.labelMat[i] * oS.K[i,j] * (oS.alphas[i] - alphaIold) - \
             oS.labelMat[j] * oS.K[j,j]*(oS.alphas[j]-alphaJold)
        if (0<oS.alphas[i]) and (oS.alphas[i]<oS.C):
            oS.b=b1
        elif (0<oS.alphas[j]) and (oS.alphas[j]<oS.C):
            oS.b=b2
        else:
            oS.b=(b1+b2)/2.0

        return 1
    else:
        return 0

def smoPlatt(dataMatIn,classLabels,C,toler,maxIter,kTup):
    ###
    oS=optStruct(np.mat(dataMatIn),np.mat(classLabels).transpose(),C,toler,kTup)
    iter=0
    entireSet=True; # flag whether go over the whole set or only the non-bounded ones
    alphaPairsChanged=0

    ### the while loop stops when either of these 2 requirements are satisfied:
    ### 1. the iteration times exceed the max value
    ### 2. no alpha pairs were changed when go over the whole set

    while (iter<maxIter) and ((alphaPairsChanged>0) or entireSet):
        alphaPairsChanged=0
        if entireSet:

            # traverse all the values in alphas, first time set entireSet to be true
            # especially for the first time, all the alpha value in alphas are updated


            for i in range(oS.m):
                alphaPairsChanged+=innerL(i,oS)
                # #print "fullSet, iter: %d, i:%d, pairs changed: %d" %\
                #   (iter,i,alphaPairsChanged)

            # iteration times add 1, unlike the simple case, here iter calculate the loop times
            # however, in the simple case, iter add 1 only when no alpha pairs were changed

            iter+=1

            # only traverse the non-bounded alphas
        else:
            nonBoundIs=np.nonzero((oS.alphas.A>0)*(oS.alphas.A<C))[0]
            for i in nonBoundIs:
                alphaPairsChanged+=innerL(i,oS)
                # #print "non-bound, iter:%d, i:%d, pairs changed:%d"%\
                #       (iter,i,alphaPairsChanged)
            iter+=1


        # if this time go over the whole set
        # only traverse the non-bounded set next time
        if entireSet:
            entireSet=False

        # when no alpha pairs where changed in the for loop for non-bounded alphas, then go over the
        # whole set of alphas next time; if there are pairs of alphas changed in the non-bounded set
        # scan the partial set again next time
        elif (alphaPairsChanged==0):
            entireSet=True

        print "iteration number : %d"% iter
    return oS.b,oS.alphas

def calcWs(alphas,dataArr,classLabels):
    X=np.mat(dataArr)
    labelMat=np.mat(classLabels).transpose()
    m,n=np.shape(X)
    w=np.zeros((n,1))
    for i in range(m):
        w+=np.multiply(alphas[i]*labelMat[i],X[i,:].T)

    return w

if __name__=="__main__":
    dataArr, labelArr = loadDataSet('testSet.txt')
    b, alphas = smoPlatt(dataArr, labelArr, 0.6, 0.001, 40,kTup=('lin',0))
    w=calcWs(alphas,dataArr,labelArr)
    print w
    dataMat=np.mat(dataArr)
    test1=dataMat[0]*np.mat(w)+b
    print test1











