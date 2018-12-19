<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>
# linear Regression

Datesets: $D=\{(x_1,y_1),...(x_m,y_m)\}$

prediction: $\hat y= wx_i+b$

cost function: $E(w,b)=\sum_{i=1}^{m}(y_i-wx_i-b)^2$

minimize cost function:

$\frac{\partial E}{\partial w}=2(w\sum_{i=1}^{m}x_i^2-\sum_{i=1}^{m}(y_i-b)x_i)=0$

$\frac{\partial E}{\partial b}=2(mb-\sum_{i=1}^{m}(y_i-wx_i))=0$

so,

$b=\frac{1}{m}\sum_{i=1}^{m}(y_i-wx_i)$

$mw\sum_{i=1}^{m}x_i^2=m\sum_{i=1}^{m}y_i(x_i-\overline x)+(\sum_{i=1}^{m}x_i)^2$

then,
$w=\frac{\sum_{i=1}^{m}y_i(x_i-\overline x)}{\sum_{i=1}^{m}x_i^2-\frac{1}{m}(\sum_{i=1}^{m}x_i)^2}$

## least square

$x$ is a multivariable with a dimension of $d$, with the expression of $x_i=(x_{i1},...x_{id})$, then the dataset can be expressed as a matrix $X$ as:
$$
\left\{
\begin{matrix}
x_{11}&...&x_{1d}&1\\
x_{21}&...&x_{2d}&1\\
\vdots  & \ddots & \vdots \\
x_{m1}&...&x_{md}&1
\end{matrix}
\right\}
=
\left\{
\begin{matrix}
x_1^T&1\\
x_2^T&1\\
\vdots&\vdots\\
x_m^T&1
\end{matrix}
\right\}
$$
and the label can also be written as vector $y=(y_1,...,y_m)^T$, then the predicted $w$ is also a vector with the expression $\hat w=(w,b)$, and the predicted label $\hat y=X\hat w$

cost function:

$E_{\hat w}=(y-X\hat w)^T(y-X\hat w)$

$\frac{\partial E_{\hat w}}{\partial \hat w}=2X^T(X\hat w-y)=0$

if $X^TX$ is full-rank matrix or positive definite determined matrix, we can obtain:

$\hat w^* = (X^Tx)^{-1}x^Ty$

## regularization terms
Since $X^Tx$ can be non-full-rank, we can introducte regularization terms.