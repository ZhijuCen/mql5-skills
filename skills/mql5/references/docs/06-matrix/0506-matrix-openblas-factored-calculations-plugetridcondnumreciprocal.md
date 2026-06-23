# PLUGeTridCondNumReciprocal

Estimates the reciprocal of the condition number of a general tridiagonal matrix A in either the one-norm or infinity-norm, using the LU factorization computed by [FactorizationPLUGeTridRaw](/en/docs/matrix/openblas/factorizations/factorizationplugetridraw). LAPACK function [GTCON](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gtcon.html).

Computing for type matrix<double>

```
bool  matrix::PLUGeTridCondNumReciprocal(
   long[]&         ipiv,          // pivot indices array
   ENUM_BLAS_NORM  norm,          // matrix norm
   double          anorm,         // matrix norm value
   double&         rcond          // condition number reciprocal
   );

```

Computing for type matrix<float>

```
bool  matrixf::PLUGeTridCondNumReciprocal(
   long[]&         ipiv,          // pivot indices array
   ENUM_BLAS_NORM  norm,          // matrix norm
   float           anorm,         // matrix norm value
   float&          rcond          // condition number reciprocal
   );

```

Computing for type matrix<complex>

```
bool  matrixc::PLUGeTridCondNumReciprocal(
   long[]&         ipiv,          // pivot indices array
   ENUM_BLAS_NORM  norm,          // matrix norm
   double          anorm,         // matrix norm value
   double&         rcond          // condition number reciprocal
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::PLUGeTridCondNumReciprocal(
   long[]&         ipiv,          // pivot indices array
   ENUM_BLAS_NORM  norm,          // matrix norm
   float           anorm,         // matrix norm value
   float&          rcond          // condition number reciprocal
   );

```

Parameters

ipiv

[in]  Pivot indices array obtained as result of GTTRF function.

norm

[in]  Value from the [ENUM_BLAS_NORM](/en/docs/matrix/openblas/factored_calculations/plucondnumreciprocal#enum_blas_norm) enumeration, which defines estimation the reciprocal of the condition number.

anorm

[in]  Matrix norm value. If norm = 'O', the one-norm of the original matrix A. If norm = 'I', the infinity-norm of the original matrix A. Norm value can be obtained with [MatrixNormGeTrid](/en/docs/matrix/openblas/blas_matrix_norm/matrixnormgetrid) of the original matrix A.

rcond

[out]  An estimate of the reciprocal of the condition number. The routine sets rcond=0 if the estimate underflows; in this case the matrix is singular (to working precision). However, anytime rcond is small compared to 1.0, for the working precision, the matrix may be poorly conditioned or even singular.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix AF obtained as result of [FactorizationPLUGeTridRaw](/en/docs/matrix/openblas/factorizations/factorizationplugetridraw) method.

The computed rcond is never less than r (the reciprocal of the true condition number) and in practice is nearly always less than 10r. A call to this routine involves solving a number of systems of linear equations A*x = b; the number is usually 4 or 5 and never more than 11

ENUM_BLAS_NORM

An enumeration defining the matrix norm.

| ID | Description |
| --- | --- |
| BLASNORM_O | 'O': One-norm |
| BLASNORM_I | 'I': Infinity-norm |
