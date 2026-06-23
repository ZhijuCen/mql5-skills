# LeastSquaresSolutionWY

Solves overdetermined or underdetermined real / complex linear systems involving an m-by-n matrix A, or its transpose / conjugate-transpose, using a QR or LQ factorization of A with compact WY representation of Q. It is assumed that A has full rank.

The following options are provided:

1. If trans = 'N' and m >= n:  find the least squares solution of an overdetermined system, i.e., solve the least squares problem minimize || B - A*X ||.

2. If trans = 'N' and m < n:  find the minimum norm solution of an underdetermined system A * X = B.

3. If trans = 'T' and m >= n:  find the minimum norm solution of an underdetermined system A**T * X = B.

4. If trans = 'T' and m < n:  find the least squares solution of an overdetermined system, i.e., solve the least squares problem minimize || B - A**T * X ||.

LAPACK function [GELST](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gelst.html).

Computing for type matrix<double>

```
bool  matrix::LeastSquaresSolutionWY(
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   matrix&             B,            // right hand side matrix B
   matrix&             X,            // solution matrix X
   matrix&             residuals     // matrix with residual sums of squares
   );
 
bool  matrix::LeastSquaresSolutionWY(
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   vector&             B,            // right hand side vector B
   vector&             X,            // solution vector X
   vector&             residuals     // vector with residual sums of squares
   );

```

Computing for type matrix<float>

```
bool  matrixf::LeastSquaresSolutionWY(
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   matrixf&            B,            // right hand side matrix B
   matrixf&            X,            // solution matrix X
   matrixf&            residuals     // matrix with residual sums of squares
   );
 
bool  matrixf::LeastSquaresSolutionWY(
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   vectorf&            B,            // right hand side vector B
   vectorf&            X,            // solution vector X
   vectorf&            residuals     // vector with residual sums of squares
   );

```

Computing for type matrix<complex>

```
bool  matrixc::LeastSquaresSolutionWY(
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   matrixc&            B,            // right hand side matrix B
   matrixc&            X,            // solution matrix X
   matrixc&            residuals     // matrix with residual sums of squares
   );
 
bool  matrixc::LeastSquaresSolutionWY(
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   vectorc&            B,            // right hand side vector B
   vectorc&            X,            // solution vector X
   vectorc&            residuals     // vector with residual sums of squares
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::LeastSquaresSolutionWY(
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   matrixcf&           B,            // right hand side matrix B
   matrixcf&           X,            // solution matrix X
   matrixcf&           residuals     // matrix with residual sums of squares
   );
 
bool  matrixcf::LeastSquaresSolutionWY(
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   vectorcf&           B,            // right hand side vector B
   vectorcf&           X,            // solution vector X
   vectorcf&           residuals     // vector with residual sums of squares
   );

```

Parameters

trans

[in]  ENUM_EQUATIONS_FORM enumeration value which specifies the form of the system of equations.

B

[in]  Matrix B whose columns are the right-hand sides for the systems of equations. Vector B contains one column of right-hand side.

X

[out]  Matrix or vector X with solutions of linear least squares problem.

residuals

[out]  Matrix or vector with the residual sum of squares for the solution in each column is given by the sum of squares of modulus of elements in that column. If trans='N' and m<=n or trans!='N' and m>=n, then residuals matrix(vector) is empty.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

If trans='N'. Matrix B must be of size m-by-nrhs, where nrhs is number of right-hand side vectors, matrix X is of size n-by-nrhs. If m>=n, matrix X contains nrhs least squares solution vectors. If m<n, matrix X contains nrhs minimum norm solution vectors.

If trans!='N'. Matrix B must be of size n-by-nrhs, matrix X is of size m-by-nrhs. If m>=n, matrix X contains nrhs minimum norm solution vectors. If m<n, matrix X contains nrhs least squares solution vectors.

The abbreviation WY is not an official acronym derived from names or mathematical terms. Compact WY representation is a historical term that originates from the original research paper where this representation was first introduced:

Schreiber, R., & Van Loan, C. (1989). A Storage-Efficient WY Representation for Products of Householder Transformations. SIAM Journal on Scientific and Statistical Computing.

To construct the matrix Q in a QR or LQ factorization, Householder reflectors are used:

Q=H1H2…Hk,

where each Hi​ is a Householder transformation. In the classical implementation, each reflector is applied individually. In the block implementation, to accelerate computations and leverage the performance benefits of BLAS, the compact WY representation is used.

ENUM_EQUATIONS_FORM

An enumeration defining which form of the equations' system calculated.

| ID | Description |
| --- | --- |
| EQUATIONSFORM_N | 'N': the linear system involves A (No transpose) |
| EQUATIONSFORM_T | 'T': the linear system involves A**T (Transpose) |
| EQUATIONSFORM_C | 'C': the linear system involves A**H (Conjugate transpose) |

In case of real matrices the value EQUATIONSFORM_C assumed as Transpose.

In case of complex matrices the value EQUATIONSFORM_T assumed as Conjugate transpose.
