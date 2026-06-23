# PLUGeTridLinearEquationsSolution

Solves a system of linear equations

A * X = B,  A**T * X = B, or  A**H * X = B

with a tridiagonal matrix A using the LU-factorization computed by [FactorizationPLUGeTridRaw](/en/docs/matrix/openblas/factorizations/factorizationplugetridraw), with multiple right-hand sides. LAPACK function [GTTRS](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gttrs.html).

Computing for type matrix<double>

```
bool  matrix::PLUGeTridLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   matrix&             B,            // right hand side matrix B
   matrix&             X             // solution matrix X
   );
 
bool  matrix::PLUGeTridLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   vector&             B,            // right hand side vector B
   vector&             X             // solution vector X
   );

```

Computing for type matrix<float>

```
bool  matrixf::PLUGeTridLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   matrixf&            B,            // right hand side matrix B
   matrixf&            X             // solution matrix X
   );
 
bool  matrixf::PLUGeTridLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   vectorf&            B,            // right hand side vector B
   vectorf&            X             // solution vector X
   );

```

Computing for type matrix<complex>

```
bool  matrixc::PLUGeTridLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   matrixc&            B,            // right hand side matrix B
   matrixc&            X             // solution matrix X
   );
 
bool  matrixc::PLUGeTridLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   vectorc&            B,            // right hand side vector B
   vectorc&            X             // solution vector X
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::PLUGeTridLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   matrixcf&           B,            // right hand side matrix B
   matrixcf&           X             // solution matrix X
   );
 
bool  matrixcf::PLUGeTridLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   ENUM_EQUATIONS_FORM trans,        // form of the system of equations
   vectorcf&           B,            // right hand side vector B
   vectorcf&           X             // solution vector X
   );

```

Parameters

ipiv

[in]  Pivot indices array obtained as result of GTTRF function.

trans

[in]  [ENUM_EQUATIONS_FORM](/en/docs/matrix/openblas/factored_calculations/plulinearequationssolution#enum_equations_form) enumeration value which specifies the form of the system of equations.

B

[in]  Matrix B whose columns are the right-hand sides for the systems of equations. Vector B contains one column of right-hand side.

X

[out]  Matrix or vector X with solutions of linear equations system.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix AF obtained as result of [FactorizationPLUGeTridRaw](/en/docs/matrix/openblas/factorizations/factorizationplugetridraw) method.

Output matrix X has the same sizes as input matrix B. Output vector X has the same size as input vector B.

ENUM_EQUATIONS_FORM

An enumeration defining which form of the equations' system calculated.

| ID | Description |
| --- | --- |
| EQUATIONSFORM_N | 'N': A * X = B  (No transpose) |
| EQUATIONSFORM_T | 'T': A**T * X = B  (Transpose) |
| EQUATIONSFORM_C | 'C': A**H * X = B  (Conjugate transpose) |

In case of real matrices the value EQUATIONSFORM_C assumed as Transpose.
