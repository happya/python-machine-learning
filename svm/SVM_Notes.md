# Supporting Vector Machine

## supporting vector

Dataset: $D=\{(x_1,y_1),...,(x_m,y_m)\},y_i\in\{-1,1\}$.

To find a plane that separates these two classes of data points.

Define the hyperplane as: $$w^Tx+b=0$$,then the distance from point  $x$ to such plane is:

$$r=\frac{wx+b}{||w||}\tag{1}$$

suppose this plane can separate those two classes, then:
$$
\begin{equation}
\left\{
\begin{array}{lc}
w^Tx_i+b\ge+1, y_i=1\\
w^Tx_i+b\le-1, y_i=-1
\end{array}
\right.
\end{equation}
\tag{2}
$$
Those points being the nearest ones satisfy the equal sign in  (2), and they are called the **supporting vectors**. The sum of distance between two supporting vectors in different classes and the hyperplane is:

$$\gamma = \frac{2}{||w||}\tag{3}$$

$\gamma$ is called the "**margin**".

> Now, the problem is find the max margin.

That is:
$$
\begin{equation}
\min\limits_{w,b} \frac{1}{2}||w||^2\\
s.t. y_i(w^Tx_i+b)\ge1, i=1,2,...,m
\end{equation}
\tag{4}
$$
And this is the **SVM model**.

## Dual problem

To solve (4), we use Lagrange multiplier method as:

$$L(w,b,\alpha) = \frac{1}{2}||w||^2+\sum\limits_{i=1}^m \alpha_i(1-y_i(w^Tx_i+b))\tag{5}$$

with $\alpha=(\alpha_1,...,\alpha_m)^T$,then:
$$
\begin{equation}

\begin{array}\\
w=\sum\limits_{i=1}^m \alpha_iy_ix_i\\
0=\sum\limits_{i=1}^m \alpha_iy_i
\end{array}
\end{equation}

\tag{6}
$$
By substituting (6) to (5), we can obtain the dual problem of (4):


$$
\begin{equation}
\begin{array}\\
\max\limits_\alpha \sum\limits_{i=1}^m \alpha_i-\frac{1}{2}\sum\limits_{i=1}^m\sum\limits_{j=1}^m \alpha_i\alpha_j y_i y_j x_i^Tx_j \\
s.t.  \sum\limits_{i=1}^m \alpha_iy_i=0, \alpha_i\ge0, i=1,2,...,m
\end{array}
\end{equation}
\tag{7}
$$
$x_i^Tx_j$ is the inner product of the vector $x_i$ and $x_j$, it can also be written as $<x_i,x_j>$.

By solving the above problem, we can obtain our SVM model as:
$$
f(x)=w^Tx+b=\sum\limits_{i=1}^m \alpha_iy_i x_i x+b\tag{8}
$$

## KKT condition

Due to the inequality constraints in (4), it should meet the KKT condition:
$$
\begin{equation}
\left\{
\begin{array}\\
\alpha_i \ge 0;\\
y_if(x_i)-1 \ge 0;\\
\alpha_i( y_if(x_i)-1)=0
\end{array}
 \right.
\end{equation}
\tag{9}
$$
From (9), we know that for $\alpha_i$ and $ y_if(x_i)-1$, at least one of them is zero. If $\alpha_i$ is zero, it makes no contribution in (8), so there must has $y_if(x_i)=1$, corresponding to those **supporting vectors**.

> Thus, only Supporting Vectors matters to the final model.

## SMO (Sequential Minimal Optimization) algorithm



To solve (7), SMO is a good algorithm.

> - choose a pair of ($\alpha_i, \alpha_j$) to be updated.
> - Fix other $\alpha$, to solve (7). ($\sum\limits_{i=1}^m \alpha_iy_i=0$)