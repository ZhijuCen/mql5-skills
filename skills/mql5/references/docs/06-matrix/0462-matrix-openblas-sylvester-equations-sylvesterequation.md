# SylvesterEquation

Solves Sylvester equation for real or complex square matrices:

A*X + X*B = scale*C

where A is m-by-m and B is n-by-n general matrices; the right hand side C and the solution X are m-by-n; and scale is an output scale factor, set <= 1 to avoid overflow in X.

LAPACK functions [GEES](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gees.html) and [TRSYL](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/trsyl.html) are used. See Note section in [SylvesterEquationSchur](/en/docs/matrix/openblas/sylvester_equations/sylvesterequationschur).

Computing for type matrix<double>

```
bool  matrix::SylvesterEquation(
   matrix&              B,            // square matrix B
   matrix&              C,            // right hand side matrix C
   matrix&              X,            // solution matrix X
   double&              scale         // scale factor
   );

```

Computing for type matrix<float>

```
bool  matrixf::SylvesterEquation(
   matrixf&             B,            // square matrix B
   matrixf&             C,            // right hand side matrix C
   matrixf&             X,            // solution matrix X
   float&               scale         // scale factor
   );

```

Computing for type matrix<complex>

```
bool  matrix::SylvesterEquation(
   matrixc&             B,            // square matrix B
   matrixc&             C,            // right hand side matrix C
   matrixc&             X,            // solution matrix X
   double&              scale         // scale factor
   );

```

Computing for type matrix<complexf>

```
bool  matrix::SylvesterEquation(
   matrixcf&            B,            // square matrix B
   matrixcf&            C,            // right hand side matrix C
   matrixcf&            X,            // solution matrix X
   float&               scale         // scale factor
   );

```

Parameters

B

[in]  Square matrix B.

C

[in]  Matrix C whose columns are the right-hand sides for the systems of equations.

X

[out]  Matrix X with solution of Sylvester equation.

scale

[out]  The scale factor, set <= 1 to avoid overflow in X.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Output matrix X has the same sizes as input matrix C.
