# LeastSquaresSolutionQRPivot

Computes the minimum-norm solution to a real or complex linear least squares problem minimize 2-norm(| b - A*x |) using a complete orthogonal factorization of A. A is an m-by-n matrix which may be rank-deficient. LAPACK function [GELSY](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gelsy.html).

Computing for type matrix<double>

```
bool  matrix::LeastSquaresSolutionQRPivot(
   matrix&         B,                // right hand side matrix B
   long[]&         jpvt,             // array with predefined permutations
   double          rcond,            // condition to determine matrix A rank
   matrix&         X,                // solution matrix X
   long[]&         jpvt_out,         // array with proceeded permutations
   long            rank              // effective rank of A
   );
 
bool  matrix::LeastSquaresSolutionQRPivot(
   vector&         B,                // right hand side vector B
   long[]&         jpvt,             // array with predefined permutations
   double          rcond,            // condition to determine matrix A rank
   vector&         X,                // solution vector X
   long[]&         jpvt_out,         // array with proceeded permutations
   long            rank              // effective rank of A
   );

```

Computing for type matrix<float>

```
bool  matrixf::LeastSquaresSolutionQRPivot(
   matrixf&        B,                // right hand side matrix B
   long[]&         jpvt,             // array with predefined permutations
   float           rcond,            // condition to determine matrix A rank
   matrixf&        X,                // solution matrix X
   long[]&         jpvt_out,         // array with proceeded permutations
   long            rank              // effective rank of A
   );
 
bool  matrixf::LeastSquaresSolutionQRPivot(
   vectorf&        B,                // right hand side vector B
   long[]&         jpvt,             // array with predefined permutations
   float           rcond,            // condition to determine matrix A rank
   vectorf&        X,                // solution vector X
   long[]&         jpvt_out,         // array with proceeded permutations
   long            rank              // effective rank of A
   );

```

Computing for type matrix<complex>

```
bool  matrixc::LeastSquaresSolutionQRPivot(
   matrixc&        B,                // right hand side matrix B
   long[]&         jpvt,             // array with predefined permutations
   double          rcond,            // condition to determine matrix A rank
   matrixc&        X,                // solution matrix X
   long[]&         jpvt_out,         // array with proceeded permutations
   long            rank              // effective rank of A
   );
 
bool  matrixc::LeastSquaresSolutionQRPivot(
   vectorc&        B,                // right hand side vector B
   long[]&         jpvt,             // array with predefined permutations
   double          rcond,            // condition to determine matrix A rank
   vectorc&        X,                // solution vector X
   long[]&         jpvt_out,         // array with proceeded permutations
   long            rank              // effective rank of A
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::LeastSquaresSolutionQRPivot(
   matrixcf&       B,                // right hand side matrix B
   long[]&         jpvt,             // array with predefined permutations
   float           rcond,            // condition to determine matrix A rank
   matrixcf&       X,                // solution matrix X
   long[]&         jpvt_out,         // array with proceeded permutations
   long            rank              // effective rank of A
   );
 
bool  matrixcf::LeastSquaresSolutionQRPivot(
   vectorcf&       B,                // right hand side vector B
   long[]&         jpvt,             // array with predefined permutations
   float           rcond,            // condition to determine matrix A rank
   vectorcf&       X,                // solution vector X
   long[]&         jpvt_out,         // array with proceeded permutations
   long            rank              // effective rank of A
   );

```

Parameters

B

[in]  Matrix B whose columns are the right-hand sides for the systems of equations. Vector B contains one column of right-hand side.

jpvt

[in]  Integer array of dimension n. If jpvt(i) != 0, the i-th column of A is permuted to the front of AP, otherwise column i is a free column. If array has zero size (or not initialized), then all the columns of A assumed to be free.

rcond

[in]  rcond is used to determine the effective rank of A, which is defined as the order of the largest leading triangular submatrix R11 (see Note 2) in the QR factorization with pivoting of A, whose estimated condition number < 1/rcond.

X

[out]  Matrix or vector X with solutions of linear least squares problem.

jpvt_out

[out]  Integer array with proceeded permutations. If jpvt(i) = k, then the i-th column of AP was the k-th column of A.

rank

[out]  The effective rank of A, that is, the order of the submatrix R11 (see Note 2). This is the same as the order of the submatrix T11 in the complete orthogonal factorization of A.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

1. Matrix B must be of size m-by-nrhs, where nrhs is number of right-hand side vectors, matrix X is of size n-by-nrhs.

2. The routine first computes a QR factorization with column pivoting:

A * P = Q * [ R11 R12 ]

[   0 R22 ]

with R11 defined as the largest leading submatrix whose estimated condition number is less than 1/rcond.  The order of R11, rank, is the effective rank of A.

Then, R22 is considered to be negligible, and R12 is annihilated by orthogonal transformations from the right, arriving at the complete orthogonal factorization:

A * P = Q * [ T11 0 ] * Z

[  0  0 ]

The minimum-norm solution is then

X = P * Z**T [ inv(T11)*Q1**T*B ]

[        0         ]

where Q1 consists of the first rank columns of Q.
