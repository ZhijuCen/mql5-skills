# BlasL3HeR2K

Performs a Hermitian rank-2k update.

CU = alpha * A * B**H + alpha * B * A**H + beta*C  or

CU = alpha * A**H * B + alpha * B**H * A + beta*C

Method BlasL3HeR2K is applied to the general matrix A. General matrices A and B have size n-by-k if parameter trans='N', or k-by-n otherwise.

BLAS function [HER2K](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/her2k.html).

Computing for type matrix<complex>

```
bool  matrix::BlasL3HeR2K(
   ENUM_BLAS_TRANS trans,         // specifies the operation
   complex         alpha,         // scalar multiplier alpha
   matrixc&        B,             // second matrix B
   complex         beta,          // scalar multiplier beta
   matrixc&        C,             // Hermitian matrix C
   matrixc&        CU             // updated matrix C
   );

```

Computing for type matrix<complexf>

```
bool  matrixf::BlasL3HeR2K(
   ENUM_BLAS_TRANS trans,         // specifies the operation
   complexf        alpha,         // scalar multiplier alpha
   matrixcf&       B,             // second matrix B
   complexf        beta,          // scalar multiplier beta
   matrixcf&       C,             // Hermitian matrix C
   matrixcf&       CU             // updated matrix C
   );

```

Parameters

trans

[in]  Value from the ENUM_BLAS_TRANS enumeration, which specifies the operation:

if transa= 'N', then CU = alpha * A * B**H + alpha * B * A**H + beta*C;

if transa= 'T', then CU = alpha * A**H * B + alpha * B**H * A + beta*C;

if transa= 'C', then CU = alpha * A**H * B + alpha * B**H * A + beta*C.

alpha

[in]  Scalar multiplier alpha.

B

[in]  General matrix B with the same size as of input matrix A.

beta

[in]  Scalar multiplier beta.

C

[in]  Hermitian matrix C of size n-by-n. It can be upper triangular or lower triangular matrix. Triangular matrices are assumed to be Hermitian.

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
