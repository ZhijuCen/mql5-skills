# FactorizationLQShortWide

Computes a blocked Short-Wide LQ factorization of an m-by-n (m<n) matrix: A = L * Q. LAPACK function [LASWLQ](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/laswlq.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationLQShortWide(
   bool            reduced,      // calculation mode reduced or complete
   long&           mb,           // row block size to be used in the blocked LQ
   long&           nb,           // column block size to be used in the blocked LQ
   matrix&         L,            // lower triangular matrix L
   matrix&         Q             // orthogonal matrix Q
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationLQShortWide(
   bool            reduced,      // calculation mode reduced or complete
   long&           mb,           // row block size to be used in the blocked LQ
   long&           nb,           // column block size to be used in the blocked LQ
   matrixf&        L,            // lower triangular matrix L
   matrixf&        Q             // orthogonal matrix Q
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationLQShortWide(
   bool            reduced,      // calculation mode reduced or complete
   long&           mb,           // row block size to be used in the blocked LQ
   long&           nb,           // column block size to be used in the blocked LQ
   matrixc&        L,            // lower triangular matrix L
   matrixc&        Q             // unitary matrix Q
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationLQShortWide(
   bool            reduced,      // calculation mode reduced or complete
   long&           mb,           // row block size to be used in the blocked LQ
   long&           nb,           // column block size to be used in the blocked LQ
   matrixcf&       L,            // lower triangular matrix L
   matrixcf&       Q             // unitary matrix Q
   );

```

Parameters

reduced

[in]  Calculation mode. If reduced is true then matrices L, Q calculated with reduced dimensions (M, K), (K, N). If reduced is false it means complete calculation of matrices L, Q with dimensions (M,N), (N,N).

mb

[in,out] The row block size to be used in the blocked LQ. M >= MB >= 1. If 0 is passed in the parameter, the optimal MB value will be calculated using the [ILAENV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ilaenv.html) function and returned.

nb

[in,out] The column block size to be used in the blocked LQ. NB > M. If 0 is passed in the parameter, the optimal NB value will be calculated using the [ILAENV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ilaenv.html) function and returned.

L

[out]  Lower triangular matrix L.

Q

[out]  Orthogonal or unitary matrix Q.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

If reduced is true, matrix L is of m-by-m sizes, matrix Q is of m-by-n sizes.

If reduced is false, matrix L is of m-by-n sizes, matrix Q is of n-by-n sizes.

Although the LAPACK routine [ILAENV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/ilaenv.html) computes suitable values for MB and NB automatically, these parameters can be tuned manually to match the CPU cache size, which may provide a significant performance improvement. A useful rule of thumb is:

MB = min(M, 32 or 64 or 128)

NB = max(2*M, cache_bytes / (sizeof(type)*M))

NB = max(NB, M + MB)

NB = min(NB, N-1)
