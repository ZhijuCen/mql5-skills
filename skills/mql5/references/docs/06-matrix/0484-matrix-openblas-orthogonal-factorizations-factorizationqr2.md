# FactorizationQR2

Computes the generalized QR factorization of two matrices - A of n-by-m size and B of n-by-p size: A = Q * R, B = Q * T * Z.

LAPACK function [GGQRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ggqrf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationQR2(
   matrix&         B,            // matrix B
   matrix&         Q,            // orthogonal matrix Q
   matrix&         R,            // upper triangular matrix R
   matrix&         T,            // upper trapezoidal matrix T
   matrix&         Z             // orthogonal matrix Z
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationQR2(
   matrixf&        B,            // matrix B
   matrixf&        Q,            // orthogonal matrix Q
   matrixf&        R,            // upper triangular matrix R
   matrixf&        T,            // upper trapezoidal matrix T
   matrixf&        Z             // orthogonal matrix Z
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationQR2(
   matrixc&        B,            // matrix B
   matrixc&        Q,            // unitary matrix Q
   matrixc&        R,            // upper triangular matrix R
   matrixc&        T,            // upper trapezoidal matrix T
   matrixc&        Z             // unitary matrix Z
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationQR2(
   matrixcf&       B,            // matrix B
   matrixcf&       Q,            // unitary matrix Q
   matrixcf&       R,            // upper triangular matrix R
   matrixcf&       T,            // upper trapezoidal matrix T
   matrixcf&       Z             // unitary matrix Z
   );

```

Parameters

B

[in]  Second matrix in the generalized QR factorization.

Q

[out]  Orthogonal or unitary matrix Q.

R

[out]  Upper triangular matrix R. If n<m, matrix R is upper trapezoidal.

T

[out]  Upper trapezoidal matrix T.

Z

[out]  Orthogonal or unitary matrix Z.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
