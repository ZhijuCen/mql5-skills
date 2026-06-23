# PLUQLinearEquationsSolution

Solves a system of linear equations

A * X = scale * RHS

with a general N-by-N matrix A using the LU-factoization with complete pivoting computed by [FactorizationPLUQRaw](/en/docs/matrix/openblas/factorizations/factorizationpluqraw). LAPACK function [GESC2](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gesc2.html).

Computing for type matrix<double>

```
bool  matrix::PLUQLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   long[]&             jpiv,         // pivot indices array
   matrix&             B,            // right hand side matrix B
   matrix&             X,            // solution matrix X
   double&             scale         // scale factor
   );
 
bool  matrix::PLUQLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   long[]&             jpiv,         // pivot indices array
   vector&             B,            // right hand side vector B
   vector&             X,            // solution vector X
   double&             scale         // scale factor
   );

```

Computing for type matrix<float>

```
bool  matrixf::PLUQLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   long[]&             jpiv,         // pivot indices array
   matrixf&            B,            // right hand side matrix B
   matrixf&            X,            // solution matrix X
   float&              scale         // scale factor
   );
 
bool  matrixf::PLUQLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   long[]&             jpiv,         // pivot indices array
   vectorf&            B,            // right hand side vector B
   vectorf&            X,            // solution vector X
   float&              scale         // scale factor
   );

```

Computing for type matrix<complex>

```
bool  matrixc::PLUQLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   long[]&             jpiv,         // pivot indices array
   matrixc&            B,            // right hand side matrix B
   matrixc&            X,            // solution matrix X
   double&             scale         // scale factor
   );
 
bool  matrixc::PLUQLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   long[]&             jpiv,         // pivot indices array
   vectorc&            B,            // right hand side vector B
   vectorc&            X,            // solution vector X
   double&             scale         // scale factor
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::PLUQLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   long[]&             jpiv,         // pivot indices array
   matrixcf&           B,            // right hand side matrix B
   matrixcf&           X,            // solution matrix X
   float&              scale         // scale factor
   );
 
bool  matrixcf::PLUQLinearEquationsSolution(
   long[]&             ipiv,         // pivot indices array
   long[]&             jpiv,         // pivot indices array
   vectorcf&           B,            // right hand side vector B
   vectorcf&           X,            // solution vector X
   float&              scale         // scale factor
   );

```

Parameters

ipiv

[in]  Rows pivot indices array obtained as result of GETC2 function.

jpiv

[in]  Columns pivot indices array obtained as result of GETC2 function.

B

[in]  Matrix B whose column is the right-hand side for the system of equations, matix B must contain only one column. Vector B contains one column of right-hand side.

X

[out]  Matrix or vector X with solutions of linear equations system.

scale

[out]  Scale factor; scale is chosen 0 <= scale <= 1 to prevent overflow in the solution.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix AF obtained as result of GETC2 function.

Output matrix X has the same sizes as input matrix B. Output vector X has the same size as input vector B.
