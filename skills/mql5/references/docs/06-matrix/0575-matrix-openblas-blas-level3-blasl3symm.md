# BlasL3SyMM

Computes a matrix-matrix product where the input matrix A is symmetric.

C = alpha*A*B + beta*C  or

C = alpha*B*A + beta*C,

where A is a symmetric matrix of m-by-m size if side='L', or n-by-n size otherwise; B and C are m-by-n matrices.

BLAS function [SYMM](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/symm.html).

Computing for type matrix<double>

```
bool  matrix::BlasL3SyMM(
   ENUM_BLAS_SIDE  side,          // specifies side of A in the product
   double          alpha,         // scalar multiplier alpha
   matrix&         B,             // matrix B
   double          beta,          // scalar multiplier beta
   matrix&         C              // result matrix C
   );

```

Computing for type matrix<float>

```
bool  matrixf::BlasL3SyMM(
   ENUM_BLAS_SIDE  side,          // specifies side of A in the product
   float           alpha,         // scalar multiplier alpha
   matrixf&        B,             // matrix B
   float           beta,          // scalar multiplier beta
   matrix&         C              // result matrix C
   );

```

Parameters

side

[in]  Value from the ENUM_BLAS_SIDE enumeration, which specifies the side of the input matrix A in the product:

if side= 'L', then C = alpha*A*B + beta*C;

if side= 'R', then C = alpha*B*A + beta*C.

alpha

[in]  Scalar multiplier alpha.

B

[in]  Matrix B of size m-by-n.

beta

[in]  Scalar multiplier beta.

C

[in, out]  Result matrix C of size m-by-n. If beta is not zero, then matrix C should contain actual data before entry.If matrix size differs from m-by-n, then matrix C will be resized and zeroed.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The input can be a symmetric, upper triangular or lower triangular matrix. Triangular matrices are assumed to be symmetric.

ENUM_BLAS_SIDE

An enumeration defining the side of the input matrix A in the product.

| ID | Description |
| --- | --- |
| BLASSIDE_L | 'L': Left side |
| BLASSIDE_R | 'R': Right side |
