# LDLSyTridPDLinearEquationsSolution

Solves a system of linear equations  A * X = B  with a real symmetric or complex Hermitian positive-definite tridiagonal matrix using the factorization A = L * D * L**T computed by [FactorizationLDLSyTridPD](/en/docs/matrix/openblas/factorizations/factorizationldlsytridpd), with multiple right-hand sides. LAPACK function [PTTRS](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/pttrs.html).

Computing for type matrix<double>

```
bool  matrix::LDLSyTridPDLinearEquationsSolution(
   matrix&             D,            // diagonal matrix
   matrix&             B,            // right hand side matrix B
   matrix&             X             // solution matrix X
   );
 
bool  matrix::LDLSyTridPDLinearEquationsSolution(
   matrix&             D,            // diagonal matrix
   vector&             B,            // right hand side vector B
   vector&             X             // solution vector X
   );

```

Computing for type matrix<float>

```
bool  matrixf::LDLSyTridPDLinearEquationsSolution(
   matrixf&            D,            // diagonal matrix
   matrixf&            B,            // right hand side matrix B
   matrixf&            X             // solution matrix X
   );
 
bool  matrixf::LDLSyTridPDLinearEquationsSolution(
   matrixf&            D,            // diagonal matrix
   vectorf&            B,            // right hand side vector B
   vectorf&            X             // solution vector X
   );

```

Computing for type matrix<complex>

```
bool  matrixc::LDLSyTridPDLinearEquationsSolution(
   matrixcd&           D,            // diagonal matrix
   matrixc&            B,            // right hand side matrix B
   matrixc&            X             // solution matrix X
   );
 
bool  matrixc::LDLSyTridPDLinearEquationsSolution(
   matrixcd&           D,            // diagonal matrix
   vectorc&            B,            // right hand side vector B
   vectorc&            X             // solution vector X
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::LDLSyTridPDLinearEquationsSolution(
   matrixcf&           D,            // diagonal matrix
   matrixcf&           B,            // right hand side matrix B
   matrixcf&           X             // solution matrix X
   );
 
bool  matrixcf::LDLSyTridPDLinearEquationsSolution(
   matrixcf&           D,            // diagonal matrix
   vectorcf&           B,            // right hand side vector B
   vectorcf&           X             // solution vector X
   );

```

Parameters

D

[in]  Diagonal matrix obtained as result of [FactorizationLDLSyTridPD](/en/docs/matrix/openblas/factorizations/factorizationldlsytridpd) method.

B

[in]  Matrix B whose columns are the right-hand sides for the systems of equations. Vector B contains one column of right-hand side.

X

[out]  Matrix or vector X with solutions of linear equations system.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix L obtained as result of [FactorizationLDLSyTridPD](/en/docs/matrix/openblas/factorizations/factorizationldlsytridpd) method.

Output matrix X has the same sizes as input matrix B. Output vector X has the same size as input vector B.
