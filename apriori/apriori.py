
# coding: utf-8

# 如果某元素是不频繁的，那么包含该元素的超集也是不频繁的

import numpy as np
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


# In[14]:

def creat_C1(dataset):
    C1 = []
    for tra in dataset:
        for item in tra:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)

def scan_D(D, Ck, minisupport):
    ssCnt = {}
    for iid in D:
        for record in Ck:
            if record.issubset(iid):
                ssCnt[record] = ssCnt.get(record,0)+1
    num = float(len(D))
    support_data = {}
    retlist = []
    for key in ssCnt:
        s = ssCnt[key]/num
        if s >= minisupport:
            retlist.insert(0,key)
            support_data[key] = s
    return retlist, support_data


# 当集合中项的个数大于0时：
# 
#    - 构建一个*k*个项组成的候选项集的列表 $C_k$  
#    - 检查数据以确认每个项集都是频繁的, 得到$L_k$
#    - 保留频繁项集并构建*k+1*项组成的候选项集列表

# In[28]:

def apriori(dataset,minSupport=0.5):
    C1 = creat_C1(dataset)
    print C1
    D = map(set, dataset)
    L1, supportData = scan_D(D,C1,minSupport)
    L = [L1]
    #print L1
    k = 2
    while (len(L[k-2])>0):
        Ck = aprioriGen(L[k-2],k)
        Lk,supK = scan_D(D,Ck,minSupport)
        #print "Ck: ",Ck,"Lk: ", Lk, "supK: ", supK
        L.append(Lk)
        supportData.update(supK)
        k+=1
    return L, supportData

# 从Lk中生成含有k个元素的候选项集
def aprioriGen(Lk,k):
    retL = []
    n = len(Lk)
    for i in range(n-1):
        for j in range(i+1,n):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retL.append(Lk[i]|Lk[j])
    return retL   


# In[29]:

dataset = loadDataSet()
L, supportData = apriori(dataset,minSupport=0.5)


def gen_Rules(L,supportData, minconf=0.7):
    big_rule_list = []
    for i in range(1,len(L)):
        for freqset in L[i]:
            H1 = [frozenset([item]) for item in freqset]
            if i>1:
                rules_from_conseq(freqset,H1,supportData,big_rule_list, minconf)
            else:
                calcconf(freqset,H1,supportData,big_rule_list,minconf)
    return big_rule_list

# P-->H 置信度计算为 supportdata(P|H)/supportdata(P)
def calcconf(freqset,H,supdata,big_rule,minconf):
    prunedH = []
    for conseq in H:
        conf = supdata[freqset]/supdata[freqset-conseq]
        if conf>=minconf:
            big_rule.append((freqset-conseq, conseq, conf))
            prunedH.append(conseq)
            print freqset-conseq, '--->',conseq, conf
    return prunedH

def rules_from_conseq(freqset,H,supdata,big_rule_list,minconf):
    print "H: ", H, "freqset: ",freqset
    m = len(H[0])
    print m
    if len(freqset)>m+1:
        Hmp1 = aprioriGen(H,m+1)
        print Hmp1
        Hmp1 = calcconf(freqset,Hmp1,supdata,big_rule_list,minconf)
        print Hmp1
        if len(Hmp1)>1:
            rules_from_conseq(freqset,Hmp1,supdata,big_rule_list,minconf)


# In[31]:

gen_Rules(L,supportData,minconf=0.7)




