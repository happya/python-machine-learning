# 高斯分布
---
多元高斯分布的一个重要的性质是：如果两个变量集合是联合高斯分布，以其中一个集合为条件的分布也是高斯分布。同样的，任何一个变量的边缘分布也是高斯分布。
首先，考虑条件概率的情形。假设 $x$ 是服从高斯分布 $N(x|\mu,\Sigma)$ 的 D 维向量，把 $x$ 划分为两个不相交的子集 $x_a,x_b$。不失一般性的，令 $x_a$ 为 $x$ 的前 M个分量，令 $x_b$ 为剩余的 D-M 个分量，得到：

$$
        \begin{pmatrix}
        x_a \\
        x_b
        \end{pmatrix}
$$
对应的均值向量$\mu$的划分：
$$
        \begin{pmatrix}
        \mu_a \\
        \mu_b
        \end{pmatrix}
$$
协方差矩阵为：
$$
        \begin{pmatrix}
        \Sigma_{aa} & \Sigma_{ab} \\
        \Sigma_{ba} & \Sigma_{bb}
        \end{pmatrix}
$$
精度矩阵$\Lambda=\Sigma^{-1}$

# 线性基函数模型
---
目标变量：t
$$t = y(w,x)+\epsilon$$
其中 $\epsilon$ 是均值为0，精度（方差的逆）为 $\beta$ 的高斯随机变量。因此可以写成：
$$p(t|x,w,\beta)=N(t|y(x,w),\beta^{−1})$$