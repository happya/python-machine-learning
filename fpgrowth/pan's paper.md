
假定有$M$个RP,$N$个AP,signal map 存储的RSS矩阵S大小为$M*N$

1. 从rss矩阵每 `行向量` 之间的相似度推断RP之间距离是否close
2. 从RSS矩阵每 `列向量` 之间的相似度推断AP之间距离是否close
3. 从矩阵元$s_{mn}$的大小推断第n个AP和第m个RP之间的距离是否close
4. 从$t-1$时刻的RSS`行`与$t$时刻的RSS`行`之间的相似度判断两个时刻的距离是否close


处理：

1. 对RSS矩阵$S$归一化，
$$\tilde {S_N} = D^{-1/2}_1\tilde S D^{-1/2}_2$$
$$\tilde s_{ij} = s_{ij}-s^{min}$$
$$D_1 = diag(d_1^1,...,d_M^1),d_m^1 = \sum_{j=1}^{N}\tilde {s_{mj}}$$
$$D_2 = diag(d_1^2,...,d_N^2),d_n^1 = \sum_{j=1}^{N}\tilde {s_{nj}}$$
2. 进行奇异值分解，得到主元
$$\tilde {S_N} = U_{M*r}\Sigma_{r*r}V_{N*r}^T$$

3. 取第二和第三个进行投影（为什么舍弃第一个？因为RSS矩阵不是centering的，导致第一个是个常数),得到RP和AP的`位置`矩阵
$$P = D_1^{-1/2}(u_2, u_3), Q = D_2^{-1/2}(u_2,u_3)$$


改进：

1.运用高斯核函数，$\tilde s_{ij} = exp(-|s_{ij}-s^{max}|^2/2\sigma^2)$
