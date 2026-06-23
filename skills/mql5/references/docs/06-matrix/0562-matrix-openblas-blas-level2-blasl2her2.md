# BlasL2HeR2

Performs a rank-2 conjugated update of a Hermitian n-by-n matrix.

AU = alpha * x * conjg(y) + conjg(alpha) * y * conjg(x) + A

BLAS function [HER2](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/her2.html).

Computing for type matrix<complex>

```
bool  matrixc::BlasL2HeR2(
   complex         alpha,         // scalar multiplier alpha
   vectorc&        X,             // vector X
   vectorc&        Y,             // vector Y
   matrixc&        AU             // updated matrix A
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::BlasL2HeR2(
   complexf        alpha,         // scalar multiplier alpha
   vectorcf&       X,             // vector X
   vectorcf&       Y,             // vector Y
   matrixcf&       AU             // updated matrix A
   );

```

Parameters

alpha

[in]  Scalar multiplier alpha.

X

[in]  Vector x of size n.

Y

[in]  Vector y of size n.

AU

[out]  Updated matrix A.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The input can be a Hermitian conjugated, upper triangular or lower triangular matrix. Triangular matrices are assumed to be Hermitian.
