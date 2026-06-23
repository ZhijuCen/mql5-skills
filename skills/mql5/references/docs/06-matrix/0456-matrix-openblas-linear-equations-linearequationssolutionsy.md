# LinearEquationsSolutionSy

Computes the solution to the system of linear equations with a symmetric or Hermitian conjugated matrix A and multiple right-hand sides. A*X = B, where A is an n-by-n symmetric or unitary matrix, the columns of matrix B are individual right-hand sides, and the columns of X are the corresponding solutions. LAPACK functions [SYSV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/sysv.html), [HESV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/hesv.html).

Computing for type matrix<double>

```
bool  matrix::LinearEquationsSolutionSy(
   matrix&         B,            // right hand side matrix B
   matrix&         X             // solution matrix X
   );
 
bool  matrix::LinearEquationsSolutionSy(
   vector&         B,            // right hand side vector B
   vector&         X             // solution vector X
   );

```

Computing for type matrix<float>

```
bool  matrix::LinearEquationsSolutionSy(
   matrixf&        B,            // right hand side matrix B
   matrixf&        X             // solution matrix X
   );
 
bool  matrix::LinearEquationsSolutionSy(
   vectorf&         B,            // right hand side vector B
   vectorf&         X             // solution vector X
   );

```

Computing for type matrix<complex>

```
bool  matrix::LinearEquationsSolutionSy(
   matrixc&        B,            // right hand side matrix B
   matrixc&        X             // solution matrix X
   );
 
bool  matrix::LinearEquationsSolutionSy(
   vectorc&        B,            // right hand side vector B
   vectorc&        X             // solution vector X
   );

```

Computing for type matrix<complexf>

```
bool  matrix::LinearEquationsSolutionSy(
   matrixcf&       B,            // right hand side matrix B
   matrixcf&       X             // solution matrix X
   );
 
bool  matrix::LinearEquationsSolutionSy(
   vectorcf&       B,            // right hand side vector B
   vectorcf&       X             // solution vector X
   );

```

Parameters

B

[in]  Matrix B whose columns are the right-hand sides for the systems of equations. Vector B contains one column of right-hand side.

X

[out]  Matrix or vector X with solutions of linear equations system.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Output matrix X has the same sizes as input matrix B. Output vector X has the same size as input vector B.

The input can be a symmetric (Hermitian conjugated), [upper triangular](/en/docs/matrix/matrix_manipulations/matrix_triu) or [lower triangular](/en/docs/matrix/matrix_manipulations/matrix_tril) matrix. Triangular matrices are assumed to be symmetric (Hermitian conjugated).
