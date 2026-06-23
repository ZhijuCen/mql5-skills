# CholeskyInverse

Computes the inverse of a real symmetric or complex Hermitian positive-definite matrix using the LLT factorization computed by [FactorizationCholesky](/en/docs/matrix/openblas/factorizations/factorizationcholesky). LAPACK function [POTRI](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/potri.html).

Computing for type matrix<double>

```
bool  matrix::CholeskyInverse(
   matrix&         AI             // inverse of matrix A
   );

```

Computing for type matrix<float>

```
bool  matrixf::CholeskyInverse(
   matrixf&        AI             // inverse of matrix A
   );

```

Computing for type matrix<complex>

```
bool  matrixc::CholeskyInverse(
   matrixc&        AI             // inverse of matrix A
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::CholeskyInverse(
   matrixcf&       AI             // inverse of matrix A
   );

```

Parameters

ipiv

[in]  Pivot indices array obtained as result of SYTRF or HETRF function.

AI

[out]  Inverted matrix.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix L obtained as result of [FactorizationCholesky](/en/docs/matrix/openblas/factorizations/factorizationcholesky) method.
