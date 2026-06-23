# Matrix Norm

This section presents functions for computing various matrix norms for different matrix structures—general (rectangular), tridiagonal, upper Hessenberg, symmetric/Hermitian (both full and tridiagonal), and triangular/trapezoidal. Each routine is templated for four data types (double, float, std::complex<double>, std::complex<float>) and overloads the signature

```
bool MatrixNorm*(ENUM_BLAS_NORMX norm, T& norm_value);

```

where norm specifies one of:

- 1‑norm (BLASNORMX_O)
- Infinity‑norm (BLASNORMX_I)
- Frobenius norm (BLASNORMX_F)
- max‑abs element (BLASNORMX_M)

Results are returned via norm_value; the function returns true on success or false on error.

Under the hood, all routines call optimized LAPACK drivers—LANGE, LANGT, LANHS, LANSY/LANHE, LANST/LANHT, and LANTR—to guarantee both high performance and numerical reliability in large‑scale linear‑algebra computations.

| Function | Action |
| --- | --- |
| MatrixNorm | Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a general rectangular matrix. LAPACK function  LANGE . |
| MatrixNormGeTrid | Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a general tridiagonal matrix. LAPACK function  LANGT . |
| MatrixNormHessenberg | Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of an upper Hessenberg matrix. LAPACK function  LANHS . |
| MatrixNormSy | Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a real symmetric or complex Hermitian matrix. LAPACK functions  LANSY ,  LANHE . |
| MatrixNormComplexSy | Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a complex symmetric (not Hermitian) matrix. LAPACK function  LANSY . |
| MatrixNormSyTrid | Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a real symmetric or complex Hermitian tridiagonal matrix. LAPACK functions  LANST ,  LANHT . |
| MatrixNormTriangular | Returns the value of the 1-norm, infinity-norm, Frobenius norm, or the largest absolute value of any element of a trapezoidal m-by-n or triangular matrix. LAPACK function  LANTR . |
