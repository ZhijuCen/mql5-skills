# LDLComplexSyLinearEquationsSolution

Solves a system of linear equations  A * X = B  with a complex symmetric indefinite matrix using the factorization A = U**T * D * U or A = L * D * L**T computed by [FactorizationLDLComplexSyRaw](/en/docs/matrix/openblas/factorizations/factorizationldlcomplexsyraw), with multiple right-hand sides. LAPACK function [SYTRS](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/sytrs.html).

Computing for type matrix<complex>

```
bool  matrixc::LDLComplexSyLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   matrixc&            B,            // right hand side matrix B
   matrixc&            X             // solution matrix X
   );
 
bool  matrixc::LDLComplexSyLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   vectorc&            B,            // right hand side vector B
   vectorc&            X             // solution vector X
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::LDLComplexSyLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   matrixcf&           B,            // right hand side matrix B
   matrixcf&           X             // solution matrix X
   );
 
bool  matrixcf::LDLComplexSyLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   vectorcf&           B,            // right hand side vector B
   vectorcf&           X             // solution vector X
   );

```

Parameters

ipiv

[in]  Pivot indices array obtained as result of SYTRF function.

B

[in]  Matrix B whose columns are the right-hand sides for the systems of equations. Vector B contains one column of right-hand side.

X

[out]  Matrix or vector X with solutions of linear equations system.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix AF obtained as result of SYTRF function.

Output matrix X has the same sizes as input matrix B. Output vector X has the same size as input vector B.
