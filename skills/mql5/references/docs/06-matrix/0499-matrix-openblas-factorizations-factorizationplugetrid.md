# FactorizationPLUGeTrid

Computes an LU factorization of a general (non-symmetric) tridiagonal N-by-N matrix A using elimination with partial pivoting and row interchanges. The factorization has the form

A = P * L * U

where P is a permutation matrix, L is lower triangular with unit diagonal elements, and U is upper triangular. LAPACK function [GTTRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gttrf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationPLUGeTrid(
   matrix&         P,            // permutation matrix P
   matrix&         L,            // lower triangular matrix L
   matrix&         U             // upper triangular matrix U
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationPLUGeTrid(
   matrixf&        P,            // permutation matrix P
   matrixf&        L,            // lower triangular matrix L
   matrixf&        U             // upper triangular matrix U
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationPLUGeTrid(
   matrixc&        P,            // permutation matrix P
   matrixc&        L,            // lower triangular matrix L
   matrixc&        U             // upper triangular matrix U
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationPLUGeTrid(
   matrixcf&       P,            // permutation matrix P
   matrixcf&       L,            // lower triangular matrix L
   matrixcf&       U             // upper triangular matrix U
   );

```

Parameters

P

[out]  Permutation matrix P.

L

[out]  Lower triangular matrix L with unit diagonal elements.

U

[out]  Upper triangular matrix U.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
