# BlasL3TrMM

Computes a matrix-matrix product where the input matrix A is triangular.

C = alpha*op(A)  or

C = alpha*B*op(A),

where A is a triangular matrix of m-by-m size if side='L', or n-by-n size otherwise; B and C are m-by-n matrices.

BLAS function [TRMM](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/trmm.html).

Computing for type matrix<double>

```
bool  matrix::BlasL3TrMM(
   ENUM_BLAS_SIDE  side,          // specifies side of A in the product
   ENUM_BLAS_TRANS transa,        // specifies option op(A)
   double          alpha,         // scalar multiplier alpha
   matrix&         B,             // matrix B
   matrix&         C              // result matrix C
   );

```

Computing for type matrix<float>

```
bool  matrixf::BlasL3TrMM(
   ENUM_BLAS_SIDE  side,          // specifies side of A in the product
   ENUM_BLAS_TRANS transa,        // specifies option op(A)
   float           alpha,         // scalar multiplier alpha
   matrixf&        B,             // matrix B
   float           beta,          // scalar multiplier beta
   matrix&         C              // result matrix C
   );

```

Computing for type matrix<complex>

```
bool  matrixc::BlasL3TrMM(
   ENUM_BLAS_SIDE  side,          // specifies side of A in the product
   ENUM_BLAS_TRANS transa,        // specifies option op(A)
   complex         alpha,         // scalar multiplier alpha
   matrixc&        B,             // matrix B
   matrixc&        C              // result matrix C
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::BlasL3TrMM(
   ENUM_BLAS_SIDE  side,          // specifies side of A in the product
   ENUM_BLAS_TRANS transa,        // specifies option op(A)
   complexf        alpha,         // scalar multiplier alpha
   matrixcf&       B,             // matrix B
   complexf        beta,          // scalar multiplier beta
   matrixcf&       C              // result matrix C
   );

```

Parameters

side

[in]  Value from the ENUM_BLAS_SIDE enumeration, which specifies the side of the input matrix A in the product:

if side= 'L', then C = alpha*op(A)*B;

if side= 'R', then C = alpha*B*op(A).

transa

[in]  Value from the ENUM_BLAS_TRANS enumeration, which specifies the operation:

if transa= 'N', then op(A) = A;

if transa= 'T', then op(A) =  A**T;

if transa= 'C', then op(A) = A**H.

B

[in]  Matrix B of size m-by-n.

C

[out]  Result matrix C of size m-by-n.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The input can be upper triangular or lower triangular matrix.

ENUM_BLAS_SIDE

An enumeration defining the side of the input matrix A in the product.

| ID | Description |
| --- | --- |
| BLASSIDE_L | 'L': Left side |
| BLASSIDE_R | 'R': Right side |

ENUM_BLAS_TRANS

An enumeration defining option op(A).

| ID | Description |
| --- | --- |
| BLASTRANS_N | 'N': No transpose |
| BLASTRANS_T | 'T': Transpose |
| BLASTRANS_C | 'C': Conjugate transpose |
