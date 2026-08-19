# BlasL3SyR2K

Performs a symmetric rank-2k update.

CU = alpha * A * B**T + alpha * B * A**T + beta*C  or

CU = alpha * A**T * B + alpha * B**T * A + beta*C

Method BlasL3SyR2K is applied to the general matrix A. General matrices A and B have size n-by-k if parameter trans='N', or k-by-n otherwise.

BLAS function [SYR2K](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/syr2k.html).

Computing for type matrix<double>

```
bool  matrix::BlasL3SyR2K(
   ENUM_BLAS_TRANS trans,         // specifies the operation
   double          alpha,         // scalar multiplier alpha
   matrix&         B,             // second matrix B
   double          beta,          // scalar multiplier beta
   matrix&         C,             // symmetric matrix C
   matrix&         CU             // updated matrix C
   );

```

Computing for type matrix<float>

```
bool  matrixf::BlasL3SyR2K(
   ENUM_BLAS_TRANS trans,         // specifies the operation
   float           alpha,         // scalar multiplier alpha
   matrixf&        B,             // second matrix B
   float           beta,          // scalar multiplier beta
   matrixf&        C,             // symmetric matrix C
   matrixf&        CU             // updated matrix C
   );

```

Parameters

trans

[in]  Value from the ENUM_BLAS_TRANS enumeration, which specifies the operation:

if transa= 'N', then CU = alpha * A * B**T + alpha * B * A**T + beta*C;

if transa= 'T', then CU = alpha * A**T * B + alpha * B**T * A + beta*C;

if transa= 'C', then CU = alpha * A**T * B + alpha * B**T * A + beta*C.

alpha

[in]  Scalar multiplier alpha.

B

[in]  General matrix B with the same size as of input matrix A.

beta

[in]  Scalar multiplier beta.

C

[in]  Symmetric matrix C of size n-by-n. It can be upper triangular or lower triangular matrix. Triangular matrices are assumed to be symmetric.

CU

[out]  Updated matrix C.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

ENUM_BLAS_TRANS

An enumeration defining the operation.

| ID | Description |
| --- | --- |
| BLASTRANS_N | 'N': No transpose |
| BLASTRANS_T | 'T': Transpose |
| BLASTRANS_C | 'C': Conjugate transpose |
