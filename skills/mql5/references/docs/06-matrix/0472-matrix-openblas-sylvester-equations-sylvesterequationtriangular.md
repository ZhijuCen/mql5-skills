# SylvesterEquationTriangular

Solves Sylvester equation for real quasi-triangular or complex triangular matrices:

op(A)*X + X*op(B) = scale*C

or

op(A)*X - X*op(B) = scale*C

where op(A) = A or A**T or A**H, and  A and B are both upper triangular. A is m-by-m and B is n-by-n; the right hand side C and the solution X are m-by-n; and scale is an output scale factor, set <= 1 to avoid overflow in X.

LAPACK function [TRSYL](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/trsyl.html).

Computing for type matrix<double>

```
bool  matrix::SylvesterEquationTriangular(
   ENUM_BLAS_TRANS      transa,       // specifies option op(A)
   ENUM_BLAS_TRANS      transb,       // specifies option op(B)
   ENUM_SYLVESTER_ISIGN isign,        // specifies the sign in the equation
   matrix&              B,            // upper triangular matrix B
   matrix&              C,            // right hand side matrix C
   matrix&              X,            // solution matrix X
   double&              scale         // scale factor
   );

```

Computing for type matrix<float>

```
bool  matrixf::SylvesterEquationTriangular(
   ENUM_BLAS_TRANS      transa,       // specifies option op(A)
   ENUM_BLAS_TRANS      transb,       // specifies option op(B)
   ENUM_SYLVESTER_ISIGN isign,        // specifies the sign in the equation
   matrixf&             B,            // upper triangular matrix B
   matrixf&             C,            // right hand side matrix C
   matrixf&             X,            // solution matrix X
   float&               scale         // scale factor
   );

```

Computing for type matrix<complex>

```
bool  matrix::SylvesterEquationTriangular(
   ENUM_BLAS_TRANS      transa,       // specifies option op(A)
   ENUM_BLAS_TRANS      transb,       // specifies option op(B)
   ENUM_SYLVESTER_ISIGN isign,        // specifies the sign in the equation
   matrixc&             B,            // upper triangular matrix B
   matrixc&             C,            // right hand side matrix C
   matrixc&             X,            // solution matrix X
   double&              scale         // scale factor
   );

```

Computing for type matrix<complexf>

```
bool  matrix::SylvesterEquationTriangular(
   ENUM_BLAS_TRANS      transa,       // specifies option op(A)
   ENUM_BLAS_TRANS      transb,       // specifies option op(B)
   ENUM_SYLVESTER_ISIGN isign,        // specifies the sign in the equation
   matrixcf&            B,            // upper triangular matrix B
   matrixcf&            C,            // right hand side matrix C
   matrixcf&            X,            // solution matrix X
   float&               scale         // scale factor
   );

```

Parameters

transa

[in]  ENUM_BLAS_TRANS enumeration value which specifies option op(A).

transb

[in]  ENUM_BLAS_TRANS enumeration value which specifies option op(B).

isign

[in]  ENUM_SYLVESTER_ISIGN enumeration value which specifies the sign in the equation.

B

[in]  Upper triangular matrix B.

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

ENUM_BLAS_TRANS

An enumeration defining options op(A) and op(B).

| ID | Description |
| --- | --- |
| BLASTRANS_N | 'N': No transpose |
| BLASTRANS_T | 'T': Transpose |
| BLASTRANS_C | 'C': Conjugate transpose |

In case of real matrices the value BLASTRANS_C assumed as Transpose.

In case of complex matrices the value BLASTRANS_T assumed as Conjugate transpose.

ENUM_SYLVESTER_ISIGN

An enumeration defining the sign in the equation.

| ID | Description |
| --- | --- |
| ISIGN_PLUS | +1: solve op(A)*X + X*op(B) = scale*C |
| ISIGN_MINUS | -1: solve op(A)*X - X*op(B) = scale*C |
