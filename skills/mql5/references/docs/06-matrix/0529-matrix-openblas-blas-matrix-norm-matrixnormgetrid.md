# MatrixNormGeTrid

Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a general tridiagonal matrix. LAPACK function [LANGT](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/langt.html).

Computing for type matrix<double>

```
bool  matrix::MatrixNormGeTrid(
   ENUM_BLAS_NORMX norm,          // matrix norm
   double&         norm_value     // matrix norm value
   );

```

Computing for type matrix<float>

```
bool  matrixf::MatrixNormGeTrid(
   ENUM_BLAS_NORMX norm,          // matrix norm
   float&          norm_value     // matrix norm value
   );

```

Computing for type matrix<complex>

```
bool  matrixc::MatrixNormGeTrid(
   ENUM_BLAS_NORMX norm,          // matrix norm
   double&         norm_value     // matrix norm value
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::MatrixNormGeTrid(
   ENUM_BLAS_NORMX norm,          // matrix norm
   float&          norm_value     // matrix norm value
   );

```

Parameters

norm

[in]  Value from the ENUM_BLAS_NORMX enumeration, which specifies the value to be returned by the routine.

norm_value

[out]  Calculated matrix norm value.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

ENUM_BLAS_NORMX

An enumeration defining which norm calculated.

| ID | Description |
| --- | --- |
| BLASNORMX_O | 'O': One-norm |
| BLASNORMX_I | 'I': Infinity-norm |
| BLASNORMX_F | 'F': Frobenius-norm |
| BLASNORMX_M | 'M': max(abs(A(i,j))) |
