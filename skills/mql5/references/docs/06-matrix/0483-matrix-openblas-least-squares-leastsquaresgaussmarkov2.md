# LeastSquaresGaussMarkov2

Solves a general Gauss-Markov linear model (GLM) problem

```
  minimize || y ||_2   subject to   d = A*x + B*y
              x

```

where A is an n-by-m matrix, B is an n-by-p matrix, and d is a given n-vector. It is assumed that m <= n <= m+p, and rank(A) = m and rank( A B) = n.

Under these assumptions, the constrained equation is always consistent, and there is a unique solution x and a minimal 2-norm solution y, which is obtained using a generalized QR factorization of the matrices (A, B) given by

```
  A = Q*(R),   B = Q*T*Z.
        (0)

```

In particular, if matrix B is square nonsingular, then the problem GLM is equivalent to the following weighted linear least squares problem

```
  minimize || inv(B)*(d-A*x) ||_2
              x

```

where inv(B) denotes the inverse of B. LAPACK function [GGGLM](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2026-0/ggglm.html).

Computing for type matrix<double>

```
bool  matrix::LeastSquaresGaussMarkov2(
   matrix&             B,            // second matrix B
   matrix&             D,            // right hand side matrix D
   matrix&             X,            // solution matrix X
   matrix&             Y             // solution matrix Y
   );
 
bool  matrix::LeastSquaresGaussMarkov2(
   matrix&             B,            // second matrix B
   vector&             D,            // right hand side vector D
   vector&             X,            // solution vector X
   vector&             Y             // solution vector Y
   );

```

Computing for type matrix<float>

```
bool  matrixf::LeastSquaresGaussMarkov2(
   matrixf&            B,            // second matrix B
   matrixf&            D,            // right hand side matrix D
   matrixf&            X,            // solution matrix X
   matrixf&            Y             // solution matrix Y
   );
 
bool  matrixf::LeastSquaresGaussMarkov2(
   matrixf&            B,            // second matrix B
   vectorf&            D,            // right hand side vector D
   vectorf&            X,            // solution vector X
   vectorf&            Y             // solution vector Y
   );

```

Computing for type matrix<complex>

```
bool  matrixc::LeastSquaresGaussMarkov2(
   matrixc&            B,            // second matrix B
   matrixc&            D,            // right hand side matrix D
   matrixc&            X,            // solution matrix X
   matrixc&            Y             // solution matrix Y
   );
 
bool  matrixc::LeastSquaresGaussMarkov2(
   matrixc&            B,            // second matrix B
   vectorc&            D,            // right hand side vector D
   vectorc&            X,            // solution vector X
   vectorc&            Y             // solution vector Y
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::LeastSquaresGaussMarkov2(
   matrixcf&           B,            // second matrix B
   matrixcf&           D,            // right hand side matrix D
   matrixcf&           X,            // solution matrix X
   matrixcf&           Y             // solution matrix Y
   );
 
bool  matrixcf::LeastSquaresGaussMarkov2(
   matrixcf&           B,            // second matrix B
   vectorcf&           D,            // right hand side vector D
   vectorcf&           X,            // solution vector X
   vectorcf&           Y             // solution vector Y
   );

```

Parameters

B

[in]  Second matrix B of the GLM problem.

D

[in]  Matrix D whose column is the right-hand side for the system of equations, matix D must contain only one column. Vector D contains one column of right-hand side.

X

[out]  Matrix or vector X with solutions of GLM problem.

Y

[out]  Matrix or vector Y with solutions of GLM problem.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Output vector X has size m, and output vector Y has size p. For matrix overloads, X has m rows and Y has p rows, with the same number of columns as D.
