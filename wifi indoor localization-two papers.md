# Bayesian compressive sensing (BCS) for compressive signal reconstruction (CSR)
---

> 这篇paper主要讲述的是，在有一个signal map或者说fingerprint database的情况下，如果有新的AP更新，如何利用crowsourcing技术实现signal map的更新。虽然文章本身说是bayesian 的compressive sensing技术，但我个人感觉就是相关向量机，即贝叶斯的稀疏核方法。

> 首先，在t-1时刻，signal map有N个指纹：包括位置($L_x,L_y$)和在该点的RSS向量$x_{t-1}$；在t时刻，跟新了一批crowsourcing的数据，其根据knn近似，可将这些RSS数据$y_t$划分到M个不同的位置($\tilde{L_x},\tilde{L_y}$)且$M<=N$,然后用这个相对于原始的N个数据的signal map来说比较稀疏的M个数据来更新signal map.

认为:

> 1. x和y都服从高斯分布
> 
> 2. $\Delta y(t) = \phi_m\Delta x_t + e_m$, $e_m$为高斯噪声$e \sim N(0,\beta^{-1})$
> 
> 3. $\phi_M$矩阵是由计算观测值和之前signal map之间地理位置和RSS向量之间的相似度(即距离)来决定的
> 
> 4. 运用贝叶斯理论，将$\Delta x_{t-1}$看做$\Delta x_t$的先验分布；
> 基于观测值$\Delta y_t$的$\Delta x_t$的条件分布则可看做$\Delta x_t$的后验分布，
> 它们都服从高斯分布: $\Delta {x_t}^n \sim N(\Delta \bar x_t, {\alpha_n}^{-1})$。
> 
> 5. 通过更新$\alpha and \beta$值，则可找出t时刻signal map的更新值。
> 

计算过程

 
$$p(\Delta x_t,\alpha,\beta|\Delta y_t) = p(\Delta x_t|\alpha,\beta,\Delta y_t)p(\alpha,\beta|\Delta y_t)$$
后验分步：知晓sparse signal change以及 前一刻的信号及噪音分布下full signal change的条件概率，也是高斯分布，
$$p(\Delta x_t|\alpha,\beta,\Delta y_t)=\
(2\pi)^(-N/2)|\Sigma|^{-1/2}exp(-1/2)(\Delta x_t-\mu)^T\Sigma^{-1}(\Delta x_t-\mu)$$
$$\mu = \beta\Sigma\Phi^T\Delta y_t, \Sigma = (\beta\Phi^T\Phi+A)^{-1}, A = diag(\alpha_1,\alpha_2,...,\alpha_N)$$
极大似然估计，然后更新：

$$\alpha_n^{new} = \frac{1-\alpha_n\Sigma_{nn}}{\mu_n^2}$$
$$\beta^{new} = \frac{M-Tr(I-A\Sigma)}{||\Delta y_t - \Phi\mu||_2^2}$$



## chameleon
---

问题： 在一个fingerpring database中，如果有AP进行了改动，那么在实际定位时，如果用了改动了的AP进行定位，就可能就会出现错误

解决方案：通过采用用部分AP的RSS来进行定位，这样，用未改动的AP组进行定位的结果将会趋向于聚于一类；而相反地，如果采用的AP的subset中包含了改动了的AP，结果趋于发散。