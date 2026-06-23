# LDLSyTridPDCondNumReciprocal

Estimates the reciprocal of the condition number of a real symmetric or complex Hermitian positive-definite tridiagonal matrix A using the LDLT factorization computed by [FactorizationLDLSyTridPD](/en/docs/matrix/openblas/factorizations/factorizationldlsytridpd). LAPACK function [PTCON](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ptcon.html).

Computing for type matrix<double>

```
bool  matrix::LDLSyTridPDCondNumReciprocal(
   matrix&         D,             // diagonal matrix
   double          anorm,         // matrix norm value
   double&         rcond          // condition number reciprocal
   );

```

Computing for type matrix<float>

```
bool  matrixf::LDLSyTridPDCondNumReciprocal(
   matrixf&        D,             // diagonal matrix
   float           anorm,         // matrix norm value
   float&          rcond          // condition number reciprocal
   );

```

Computing for type matrix<complex>

```
bool  matrixc::LDLSyTridPDCondNumReciprocal(
   matrixc&        D,             // diagonal matrix
   double          anorm,         // matrix norm value
   double&         rcond          // condition number reciprocal
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::LDLSyTridPDCondNumReciprocal(
   matrixcf&       D,             // diagonal matrix
   float           anorm,         // matrix norm value
   float&          rcond          // condition number reciprocal
   );

```

Parameters

D

[in]  Diagonal matrix obtained as result of [FactorizationLDLSyTridPD](/en/docs/matrix/openblas/factorizations/factorizationldlsytridpd) method.

anorm

[in]  Matrix one-norm value. Norm value can be obtained with [MatrixNormSyTrid](/en/docs/matrix/openblas/blas_matrix_norm/matrixnormsytrid) of the original matrix A.

rcond

[out]  An estimate of the reciprocal of the condition number. The routine sets rcond=0 if the estimate underflows; in this case the matrix is singular (to working precision). However, anytime rcond is small compared to 1.0, for the working precision, the matrix may be poorly conditioned or even singular.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix L obtained as result of [FactorizationLDLSyTridPD](/en/docs/matrix/openblas/factorizations/factorizationldlsytridpd) method.

The computed rcond is never less than r (the reciprocal of the true condition number) and in practice is nearly always less than 10r. A call to this routine involves solving a number of systems of linear equations A*x = b; the number is usually 4 or 5 and never more than 11
