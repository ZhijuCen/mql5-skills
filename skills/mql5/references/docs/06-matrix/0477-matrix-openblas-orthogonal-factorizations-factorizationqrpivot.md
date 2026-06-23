# FactorizationQRPivot

Computes the QR factorization of a general m-by-n matrix with column pivoting: A * P = Q * R. LAPACK function [GEQP3](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/geqp3.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationQRPivot(
   bool            reduced,      // calculation mode reduced or complete
   long[]&         jpvt,         // array with predefined permutations
   matrix&         Q,            // orthogonal matrix Q
   matrix&         R,            // upper triangular matrix R
   matrix&         P             // permutation matrix
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationQRPivot(
   bool            reduced,      // calculation mode reduced or complete
   long[]&         jpvt,         // array with predefined permutations
   matrixf&        Q,            // orthogonal matrix Q
   matrixf&        R,            // upper triangular matrix R
   matrixf&        P             // permutation matrix
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationQRPivot(
   bool            reduced,      // calculation mode reduced or complete
   long[]&         jpvt,         // array with predefined permutations
   matrixc&        Q,            // unitary matrix Q
   matrixc&        R,            // upper triangular matrix R
   matrixc&        P             // permutation matrix
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationQRPivot(
   bool            reduced,      // calculation mode reduced or complete
   long[]&         jpvt,         // array with predefined permutations
   matrixcf&       Q,            // unitary matrix Q
   matrixcf&       R,            // upper triangular matrix R
   matrixcf&       P             // permutation matrix
   );

```

Parameters

reduced

[in]  Calculation mode. If reduced is true then matrices Q, R calculated with dimensions (M, K), (K, N). If reduced is false it means complete calculation of matrices Q, R with dimensions (M,M), (M,N).

jpvt

[in]  Integer array of dimension n. if jpvt(i) ≠ 0, the i-th column of A is moved to the beginning of AP before the computation, and fixed in place during the computation. If jpvt(i) = 0, the i-th column of A is a free column (that is, it may be interchanged during the computation with any other free column). If array has zero size (or not initialized), then all the columns of A assumed to be free.

Q

[out]  Orthogonal or unitary matrix Q.

R

[out]  Upper triangular matrix R.

P

[out]  Permutation matrix P of n-by-n sizes.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

If reduced is true

If m >= n, matrix Q is of m-by-n sizes, matrix R is of n-by-n sizes.

If m < n, matrix Q is of m-by-m sizes, matrix R is of m-by-n sizes.

If reduced is false, matrix Q is of m-by-m sizes, matrix R is of m-by-n sizes.
