# FactorizationRQ2

Computes the generalized RQ factorization of an m-by-n matrix A and a p-by-n matrix B: A = R * Q, B = Z * T * Q.

LAPACK function [GGRQF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ggrqf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationRQ2(
   matrix&         B,            // matrix B
   matrix&         R,            // upper triangular matrix R
   matrix&         Q,            // orthogonal matrix Q
   matrix&         Z,            // orthogonal matrix Z
   matrix&         T             // upper trapezoidal matrix T
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationRQ2(
   matrixf&        B,            // matrix B
   matrixf&        R,            // upper triangular matrix R
   matrixf&        Q,            // orthogonal matrix Q
   matrixf&        Z,            // orthogonal matrix Z
   matrixf&        T             // upper trapezoidal matrix T
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationRQ2(
   matrixc&        B,            // matrix B
   matrixc&        R,            // upper triangular matrix R
   matrixc&        Q,            // unitary matrix Q
   matrixc&        Z,            // unitary matrix Z
   matrixc&        T             // upper trapezoidal matrix T
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationRQ2(
   matrixcf&       B,            // matrix B
   matrixcf&       R,            // upper triangular matrix R
   matrixcf&       Q,            // unitary matrix Q
   matrixcf&       Z,            // unitary matrix Z
   matrixcf&       T             // upper trapezoidal matrix T
   );

```

Parameters

B

[in]  Second matrix in the generalized RQ factorization.

R

[out]  Upper triangular matrix R. If m>n, matrix R is upper trapezoidal.

Q

[out]  Orthogonal or unitary matrix Q.

Z

[out]  Orthogonal or unitary matrix Z.

T

[out]  Upper trapezoidal matrix T.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
