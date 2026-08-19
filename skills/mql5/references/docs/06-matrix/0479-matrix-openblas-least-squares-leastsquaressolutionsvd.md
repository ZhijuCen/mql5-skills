# LeastSquaresSolutionSVD

Computes the minimum-norm solution to a real or complex linear least squares problem minimize 2-norm(| b - A*x |) using the singular value decomposition ([SVD](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqr)) of A. A is an m-by-n matrix which may be rank-deficient. LAPACK function [GELSS](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gelss.html).

Computing for type matrix<double>

```
bool  matrix::LeastSquaresSolutionSVD(
   matrix&         B,                // right hand side matrix B
   double          rcond,            // condition to determine matrix A rank
   matrix&         X,                // solution matrix X
   matrix&         residuals,        // matrix with residual sums of squares
   vector&         singular_values,  // vector of singular values
   long            rank              // effective rank of A
   );
 
bool  matrix::LeastSquaresSolutionSVD(
   vector&         B,                // right hand side vector B
   double          rcond,            // condition to determine matrix A rank
   vector&         X,                // solution vector X
   vector&         residuals,        // vector with residual sums of squares
   vector&         singular_values,  // vector of singular values
   long            rank              // effective rank of A
   );

```

Computing for type matrix<float>

```
bool  matrixf::LeastSquaresSolutionSVD(
   matrixf&        B,                // right hand side matrix B
   float           rcond,            // condition to determine matrix A rank
   matrixf&        X,                // solution matrix X
   matrixf&        residuals,        // matrix with residual sums of squares
   vectorf&        singular_values,  // vector of singular values
   long            rank              // effective rank of A
   );
 
bool  matrixf::LeastSquaresSolutionSVD(
   vectorf&        B,                // right hand side vector B
   float           rcond,            // condition to determine matrix A rank
   vectorf&        X,                // solution vector X
   vectorf&        residuals,        // vector with residual sums of squares
   vectorf&        singular_values,  // vector of singular values
   long            rank              // effective rank of A
   );

```

Computing for type matrix<complex>

```
bool  matrixc::LeastSquaresSolutionSVD(
   matrixc&        B,                // right hand side matrix B
   double          rcond,            // condition to determine matrix A rank
   matrixc&        X,                // solution matrix X
   matrixc&        residuals,        // matrix with residual sums of squares
   vector&         singular_values,  // vector of singular values
   long            rank              // effective rank of A
   );
 
bool  matrixc::LeastSquaresSolutionSVD(
   vectorc&        B,                // right hand side vector B
   double          rcond,            // condition to determine matrix A rank
   vectorc&        X,                // solution vector X
   vectorc&        residuals,        // vector with residual sums of squares
   vector&         singular_values,  // vector of singular values
   long            rank              // effective rank of A
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::LeastSquaresSolutionSVD(
   matrixcf&       B,                // right hand side matrix B
   float           rcond,            // condition to determine matrix A rank
   matrixcf&       X,                // solution matrix X
   matrixcf&       residuals,        // matrix with residual sums of squares
   vectorf&        singular_values,  // vector of singular values
   long            rank              // effective rank of A
   );
 
bool  matrixcf::LeastSquaresSolutionSVD(
   vectorcf&       B,                // right hand side vector B
   float           rcond,            // condition to determine matrix A rank
   vectorcf&       X,                // solution vector X
   vectorcf&       residuals,        // vector with residual sums of squares
   vectorf&        singular_values,  // vector of singular values
   long            rank              // effective rank of A
   );

```

Parameters

B

[in]  Matrix B whose columns are the right-hand sides for the systems of equations. Vector B contains one column of right-hand side.

rcond

[in]  rcond is used to determine the effective rank of A. Singular values S(i) <= rcond*S(1) are treated as zero. If rcond < 0, machine precision is used instead.

X

[out]  Matrix or vector X with solutions of linear least squares problem.

residuals

[out]  Matrix or vector with the residual sum of squares for the solution in each column is given by the sum of squares of elements in that column. If m<=n, then residuals matrix(vector) is empty.

singular_values

[out] Vector of computed singular values.

rank

[out]  The effective rank of A, i.e., the number of singular values which are greater than rcond*S(1).

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Matrix B must be of size m-by-nrhs, where nrhs is number of right-hand side vectors, matrix X is of size n-by-nrhs.

The condition number of A in the 2-norm = S(1)/S(min(m,n)).
