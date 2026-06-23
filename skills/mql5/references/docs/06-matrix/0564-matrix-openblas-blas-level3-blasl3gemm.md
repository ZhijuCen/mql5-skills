# BlasL3GeMM

Computes a matrix-matrix product with general matrices.

C = alpha * op(A) * op(B) + beta * C

where C is m-by-n matrix, op(A) is m-by-k matrix, op(B) is k-by-n matrix.

Method BlasL3GeMM is applied to the matrix A. Matrix A has size m-by-k if parameter transa='N', or k-by-m otherwise.

BLAS function [GEMM](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gemm-001.html).

Computing for type matrix<double>

```
bool  matrix::BlasL3GeMM(
   ENUM_BLAS_TRANS transa,        // specifies option op(A)
   ENUM_BLAS_TRANS transb,        // specifies option op(B)
   double          alpha,         // scalar multiplier alpha
   matrix&         B,             // matrix B
   double          beta,          // scalar multiplier beta
   matrix&         C              // result matrix C
   );

```

Computing for type matrix<float>

```
bool  matrixf::BlasL3GeMM(
   ENUM_BLAS_TRANS transa,        // specifies option op(A)
   ENUM_BLAS_TRANS transb,        // specifies option op(B)
   float           alpha,         // scalar multiplier alpha
   matrixf&        B,             // matrix B
   float           beta,          // scalar multiplier beta
   matrixf&        C              // result matrix C
   );

```

Computing for type matrix<complex>

```
bool  matrixc::BlasL3GeMM(
   ENUM_BLAS_TRANS transa,        // specifies option op(A)
   ENUM_BLAS_TRANS transb,        // specifies option op(B)
   complex         alpha,         // scalar multiplier alpha
   matrixc&        B,             // matrix B
   complex         beta,          // scalar multiplier beta
   matrixc&        C              // result matrix C
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::BlasL3GeMM(
   ENUM_BLAS_TRANS transa,        // specifies option op(A)
   ENUM_BLAS_TRANS transb,        // specifies option op(B)
   complexf        alpha,         // scalar multiplier alpha
   matrixcf&       B,             // matrix B
   complexf        beta,          // scalar multiplier beta
   matrixcf&       C              // result matrix C
   );

```

Parameters

transa

[in]  Value from the ENUM_BLAS_TRANS enumeration, which specifies the operation:

if transa= 'N', then op(A) = A;

if transa= 'T', then op(A) =  A**T;

if transa= 'C', then op(A) = A**H.

transb

[in]  Value from the ENUM_BLAS_TRANS enumeration, which specifies the operation:

if transa= 'N', then op(B) = B;

if transa= 'T', then op(B) =  B**T;

if transa= 'C', then op(B) = B**H.

alpha

[in]  Scalar multiplier alpha.

B

[in]  Matrix B of size k-by-n if transb='N', or of size n-by-k otherwise.

beta

[in]  Scalar multiplier beta.

C

[in,out]  Result matrix C of size m-by-n. If beta is not zero, then matrix C should contain actual data before entry.If matrix size differs from m-by-n, then matrix C will be resized and zeroed.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

ENUM_BLAS_TRANS

An enumeration defining options op(A) and op(B).

| ID | Description |
| --- | --- |
| BLASTRANS_N | 'N': No transpose |
| BLASTRANS_T | 'T': Transpose |
| BLASTRANS_C | 'C': Conjugate transpose |
