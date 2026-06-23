# FactorizationRZ

Reduces the M-by-N ( M<=N ) real or complex upper trapezoidal matrix A to upper triangular form by means of orthogonal transformations. The upper trapezoidal matrix A is factored as

A = ( R  0 ) * Z,

where Z is an N-by-N orthogonal or unitary matrix and R is an M-by-M upper triangular matrix.

LAPACK function [TZRZF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/tzrzf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationRZ(
   matrix&         R,            // upper triangular matrix R
   matrix&         Z             // orthogonal matrix Z
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationRZ(
   matrixf&        R,            // upper triangular matrix R
   matrixf&        Z             // orthogonal matrix Z
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationRZ(
   matrixc&        R,            // upper triangular matrix R
   matrixc&        Z             // unitary matrix Z
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationRZ(
   matrixcf&       R,            // upper triangular matrix R
   matrixcf&       Z             // unitary matrix Z
   );

```

Parameters

R

[out]  Upper triangular matrix R.

Z

[out]  Orthogonal or unitary matrix Z.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

If m<n matrix R is upper trapezoidal m-by-n matrix, where right n-m columns contain zeros.
