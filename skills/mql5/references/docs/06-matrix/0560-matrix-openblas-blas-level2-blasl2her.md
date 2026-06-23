# BlasL2HeR

Performs a rank-1 conjugated update of a Hermitian n-by-n matrix.

AU = alpha * x * conjg(x) + A

BLAS function [HER](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/her.html).

Computing for type matrix<complex>

```
bool  matrixc::BlasL2HeR(
   complex         alpha,         // scalar multiplier alpha
   vectorc&        X,             // vector X
   matrixc&        AU             // updated matrix A
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::BlasL2HeR(
   complexf        alpha,         // scalar multiplier alpha
   vectorcf&       X,             // vector X
   matrixcf&       AU             // updated matrix A
   );

```

Parameters

alpha

[in]  Scalar multiplier alpha.

X

[in]  Vector x of size n.

AU

[out]  Updated matrix A.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The input can be a Hermitian conjugated, upper triangular or lower triangular matrix. Triangular matrices are assumed to be Hermitian.
