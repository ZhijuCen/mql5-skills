# LDLCondNumReciprocal

Estimates the reciprocal of the condition number of a real symmetric or complex Hermitian indefinite matrix A, using the LDLT factorization computed by [FactorizationLDLRaw](/en/docs/matrix/openblas/factorizations/factorizationldlraw). LAPACK functions [SYCON](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/sycon.html), [HECON](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/hecon.html).

Computing for type matrix<double>

```
bool  matrix::LDLCondNumReciprocal(
   long[]&         ipiv,          // pivot indices array
   double          anorm,         // matrix norm value
   double&         rcond          // condition number reciprocal
   );

```

Computing for type matrix<float>

```
bool  matrixf::LDLCondNumReciprocal(
   long[]&         ipiv,          // pivot indices array
   float           anorm,         // matrix norm value
   float&          rcond          // condition number reciprocal
   );

```

Computing for type matrix<complex>

```
bool  matrixc::LDLCondNumReciprocal(
   long[]&         ipiv,          // pivot indices array
   double          anorm,         // matrix norm value
   double&         rcond          // condition number reciprocal
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::LDLCondNumReciprocal(
   long[]&         ipiv,          // pivot indices array
   float           anorm,         // matrix norm value
   float&          rcond          // condition number reciprocal
   );

```

Parameters

ipiv

[in]  Pivot indices array obtained as result of SYTRF or HETRF function.

anorm

[in]  Matrix one-norm value. Norm value can be obtained with [MatrixNormSy](/en/docs/matrix/openblas/blas_matrix_norm/matrixnormsy) of the original matrix A.

rcond

[out]  An estimate of the reciprocal of the condition number. The routine sets rcond=0 if the estimate underflows; in this case the matrix is singular (to working precision). However, anytime rcond is small compared to 1.0, for the working precision, the matrix may be poorly conditioned or even singular.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix AF obtained as result of SYTRF or HETRF function.

The computed rcond is never less than r (the reciprocal of the true condition number) and in practice is nearly always less than 10r. A call to this routine involves solving a number of systems of linear equations A*x = b; the number is usually 4 or 5 and never more than 11
