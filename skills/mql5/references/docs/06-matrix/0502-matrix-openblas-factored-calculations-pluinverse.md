# PLUInverse

Computes the inverse of an LU-factored general matrix AF computed by [FactorizationPLURaw](/en/docs/matrix/openblas/factorizations/factorizationpluraw). LAPACK function [GETRI](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/getri.html).

Computing for type matrix<double>

```
bool  matrix::PLUInverse(
   long[]&         ipiv,          // pivot indices array
   matrix&         AI             // inverse of matrix A
   );

```

Computing for type matrix<float>

```
bool  matrixf::PLUInverse(
   long[]&         ipiv,          // pivot indices array
   matrixf&        AI             // inverse of matrix A
   );

```

Computing for type matrix<complex>

```
bool  matrixc::PLUInverse(
   long[]&         ipiv,          // pivot indices array
   matrixc&        AI             // inverse of matrix A
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::PLUInverse(
   long[]&         ipiv,          // pivot indices array
   matrixcf&       AI             // inverse of matrix A
   );

```

Parameters

ipiv

[in]  Pivot indices array obtained as result of GETRF function.

AI

[out]  Inverted matrix.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

This method is applied to the matrix AF obtained as result of GETRF function.
