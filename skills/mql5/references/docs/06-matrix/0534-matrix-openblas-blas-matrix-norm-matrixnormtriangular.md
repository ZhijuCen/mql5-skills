# MatrixNormTriangular

Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a trapezoidal m-by-n or triangular matrix. LAPACK function [LANTR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/lantr.html).

Computing for type matrix<double>

```
bool  matrix::MatrixNormTriangular(
   ENUM_BLAS_NORMX norm,          // matrix norm
   double&         norm_value     // matrix norm value
   );

```

Computing for type matrix<float>

```
bool  matrixf::MatrixNormTriangular(
   ENUM_BLAS_NORMX norm,          // matrix norm
   float&          norm_value     // matrix norm value
   );

```

Computing for type matrix<complex>

```
bool  matrixc::MatrixNormTriangular(
   ENUM_BLAS_NORMX norm,          // matrix norm
   double&         norm_value     // matrix norm value
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::MatrixNormTriangular(
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

Note

Matrix is triangular if m = n. It can be both upper or lower triangular.

If m < n then matrix must be upper trapezoidal, ie lower m-by-m triangular part must contain zeroes.

If m > n then matrix must be lower trapezoidal, ie upper n-by-n triangular part must contain zeroes.

ENUM_BLAS_NORMX

An enumeration defining which norm calculated.

| ID | Description |
| --- | --- |
| BLASNORMX_O | 'O': One-norm |
| BLASNORMX_I | 'I': Infinity-norm |
| BLASNORMX_F | 'F': Frobenius-norm |
| BLASNORMX_M | 'M': max(abs(A(i,j))) |
