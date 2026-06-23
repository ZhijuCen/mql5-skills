# BlasL2HeMV

Computes a matrix-vector product for a Hermitian n-by-n matrix.

y = alpha*A*x + beta*y

BLAS function [HEMV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/hemv.html).

Computing for type matrix<complex>

```
bool  matrix::BlasL2HeMV(
   complex         alpha,         // scalar multiplier alpha
   vectorc&        X,             // vector X
   complex         beta,          // scalar multiplier beta
   vectorc&        Y              // result vector Y
   );

```

Computing for type matrix<complexf>

```
bool  matrixf::BlasL2HeMV(
   complexf        alpha,         // scalar multiplier alpha
   vectorcf&       X,             // vector X
   complexf        beta,          // scalar multiplier beta
   vectorcf&       Y              // result vector Y
   );

```

Parameters

alpha

[in]  Scalar multiplier alpha.

X

[in]  Vector x of size n.

beta

[in]  Scalar multiplier beta.

Y

[in, out]  Result vector y of size n. If beta is not zero, then vector Y should contain actual data before entry.If vector size differs from n, then vector Y will be resized and zeroed.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The input can be a Hermitian conjugated, upper triangular or lower triangular matrix. Triangular matrices are assumed to be Hermitian.
