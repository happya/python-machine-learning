# coding:utf-8
# author: yyiust


import numpy as np


def load_simple_dataset():
    simp_dset = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simp_dset

def create_init_set(dataset):
    res = {}
    for trans in dataset:
        res[frozenset(trans)] = 1
    return res


# 建造FP树节点类
class treeNode():
    def __init__(self,name,num_occur,parent_node):
        self.name = name
        self.count = num_occur
        self.nodelink = None
        self.parent = parent_node
        self.children = {}

    def inc(self,num_occur):
        self.count += num_occur

    def disp(self,ind=1):
        print ' '*ind, self.name,':', ' ', self.count
        for child in self.children.values():
            child.disp(ind+1)
# 第一次遍历数据，得到每个元素项的出现频率
# 去掉不满足最小支持度的元素项
# 构建FP树: 读入每一个项集并将其添加到一套已经存在的路径中
# 为解决相同项出现不止一次的问题，在将集合添加到树回去，先对每个集合进行排序，基于元素项的绝对出现频率来进行

def create_tree(dataset,min_sup_times=1):
    # header: 头指针表,用来指向给定类型的第一个实例
    header = {}
    # 将数据遍历一次并记录每个元素出现的频率
    for trans in dataset:
        for item in trans:
            header[item] = header.get(item,0)+1
    # 去掉不满足最小支持度的元素
    for key in header.keys():
        if header[key]<min_sup_times:
            del(header[key])
    freq_item_set = set(header.keys())
    if not freq_item_set:
        return None,None
    
    # 开始构建FP树
    # header每一个键值记录了其出现次数和是否包含在树中
    for key in header:
        header[key] = [header[key], None]
    return_tree = treeNode('Null set',1, None)
    print "headers: ", header
    # 对每一个元素项计数并排序
    # count是每条完整记录出现的次数
    for trans_set, count in dataset.items():
        print trans_set
        localD = {}
        for item in trans_set:
            if item in freq_item_set:
                localD[item] = header[item][0]
        
        # 对每一条记录，将该记录中符合要求的元素项按照总出现次数排序
        if localD:
            ordered_items = [d[0] for d in sorted(localD.items(),key=lambda p: p[1],reverse=True)]
            print "ordered_items: ", ordered_items
            update_tree(ordered_items,return_tree,header,count)
            return_tree.disp()
    return return_tree,header


def update_tree(items,tree,header,count):
    # 从第一个元素开始
    # 如果已经记录在树的孩子里了，就直接增加该元素项的次数,注意，这里的次数是count，即该条记录出现的次数
    # 对每一条记录开始，这个孩子其实是根节点
    if items[0] in tree.children:
        tree.children[items[0]].inc(count)

    # 否则，给树的孩子增加一个键
    # 
    else:
        tree.children[items[0]] = treeNode(items[0],count,tree)
        # 更新头指针表
        # 如果该头指针第一次出现，则指向它；
        # 否则，更新该头指针链表
        # (treeNode类中nodelink的作用在这里体现了，从头指针的nodelink开始，一直沿着nodelink到链表末尾)
        if not header[items[0]][1]:
            header[items[0]][1] = tree.children[items[0]]
        else:
            update_header(header[items[0]][1],tree.children[items[0]])

    if len(items)>1:
        update_tree(items[1::],tree.children[items[0]],header,count)

# 确保节点链接指向树中该元素项的每一个实例
def update_header(node_to_test,target_node):
    while node_to_test.nodelink:
        node_to_test = node_to_test.nodelink
    node_to_test.nodelink = target_node



dataset = load_simple_dataset()
init_set = create_init_set(dataset)
# print "initial set: ", init_set
mytree,myheader = create_tree(init_set,3)
#mytree.disp()

for key in myheader.keys():
    print '*****************************'
    myheader[key][1].disp()