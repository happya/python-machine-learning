# Indoor Positioning and Distance-aware Graph-based Semi-supervised Learning Method

RP分为$l$个确定的(labeled data)和$u$个不确定的(unlabeled data)
$M$个APs
构造有权图G(V,E)
V是RSS向量构成的矩阵$V=(r_1,r_2,...,r_{l+u})$,$r_i$是$M*1$的向量
E是位置向量构成的矩阵$B = (b_1,...b_l,0,...,0)$, $b_i=[x,y]^T$

综合信号传播模型和graph构造cost function
运用梯度下降算法，更新矩阵B