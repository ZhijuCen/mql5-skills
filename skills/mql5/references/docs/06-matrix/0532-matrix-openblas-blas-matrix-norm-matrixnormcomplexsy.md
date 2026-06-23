# MatrixNormComplexSy

Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a complex symmetric (not Hermitian) matrix. LAPACK function [LANSY](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/lansy.html).

Computing for type matrix<complex>

```
bool  matrixc::MatrixNormComplexSy(
   ENUM_BLAS_NORMX norm,          // matrix norm
   double&         norm_value     // matrix norm value
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::MatrixNormComplexSy(
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

The input can be a symmetric, upper triangular or lower triangular matrix. Triangular matrices are assumed to be symmetric.

ENUM_BLAS_NORMX

An enumeration defining which norm calculated.

| ID | Description |
| --- | --- |
| BLASNORMX_O | 'O': One-norm |
| BLASNORMX_I | 'I': Infinity-norm |
| BLASNORMX_F | 'F': Frobenius-norm |
| BLASNORMX_M | 'M': max(abs(A(i,j))) |
