# FactorizationQRTallSkinny

Computes a blocked Tall-Skinny QR factorization of an m-by-n (m>n) matrix: A = Q * R. LAPACK function [LATSQR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/latsqr.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationQRTallSkinny(
   long&           mb,           // row block size to be used in the blocked QR
   long&           nb,           // column block size to be used in the blocked QR
   matrix&         Q,            // orthogonal matrix Q
   matrix&         R             // upper triangular matrix R
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationQRTallSkinny(
   long&           mb,           // row block size to be used in the blocked QR
   long&           nb,           // column block size to be used in the blocked QR
   matrixf&        Q,            // orthogonal matrix Q
   matrixf&        R             // upper triangular matrix R
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationQRTallSkinny(
   long&           mb,           // row block size to be used in the blocked QR
   long&           nb,           // column block size to be used in the blocked QR
   matrixc&        Q,            // unitary matrix Q
   matrixc&        R             // upper triangular matrix R
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationQRTallSkinny(
   long&           mb,           // row block size to be used in the blocked QR
   long&           nb,           // column block size to be used in the blocked QR
   matrixcf&       Q,            // unitary matrix Q
   matrixcf&       R             // upper triangular matrix R
   );

```

Parameters

mb

[in,out] The row block size to be used in the blocked QR. MB > N. If 0 is passed in the parameter, the optimal MB value will be calculated using the [ILAENV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ilaenv.html) function and returned.

nb

[in,out] The column block size to be used in the blocked QR. N >= NB >= 1. If 0 is passed in the parameter, the optimal NB value will be calculated using the [ILAENV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ilaenv.html) function and returned.

Q

[out]  Orthogonal or unitary matrix Q.

R

[out]  Upper triangular matrix R.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Although the LAPACK routine [ILAENV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ilaenv.html) computes suitable values for MB and NB automatically, these parameters can be tuned manually to match the CPU cache size, which may provide a significant performance improvement. A useful rule of thumb is:

NB = min(N, 32 or 64)

MB = max(2*N, cache_target_rows)

MB = min(M-1, MB)

где cache_target_rows выбирается так, чтобы блок MB x N помещался в L2/L3 cache: MB ≈ cache_bytes / (8 * N) для double precision.
