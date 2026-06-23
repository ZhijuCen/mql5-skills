# BlasL2GeRC

Performs a rank-1 conjugated update of a general m-by-n matrix.

AU = alpha * x * conjg(y) + A

BLAS function [GERC](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gerc.html).

Computing for type matrix<complex>

```
bool  matrixc::BlasL2GeRC(
   complex         alpha,         // scalar multiplier alpha
   vectorc&        X,             // vector X
   vectorc&        Y,             // vector Y
   matrixc&        AU             // updated matrix A
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::BlasL2GeRC(
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

[in]  Vector x of size m.

Y

[in]  Vector y of size n.

AU

[out]  Updated matrix A.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
