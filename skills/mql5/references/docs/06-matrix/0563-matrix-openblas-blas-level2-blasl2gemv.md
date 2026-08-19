# BlasL2GeMV

Computes a matrix-vector product using a general m-by-n matrix.

y = alpha * op(A) * x + beta * y

BLAS function [GEMV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gemv.html).

Computing for type matrix<double>

```
bool  matrix::BlasL2GeMV(
   ENUM_BLAS_TRANS trans,         // specifies option op(A)
   double          alpha,         // scalar multiplier alpha
   vector&         X,             // vector X
   double          beta,          // scalar multiplier beta
   vector&         Y              // result vector Y
   );

```

Computing for type matrix<float>

```
bool  matrixf::BlasL2GeMV(
   ENUM_BLAS_TRANS trans,         // specifies option op(A)
   float           alpha,         // scalar multiplier alpha
   vectorf&        X,             // vector X
   float           beta,          // scalar multiplier beta
   vectorf&        Y              // result vector Y
   );

```

Computing for type matrix<complex>

```
bool  matrixc::BlasL2GeMV(
   ENUM_BLAS_TRANS trans,         // specifies option op(A)
   complex         alpha,         // scalar multiplier alpha
   vectorc&        X,             // vector X
   complex         beta,          // scalar multiplier beta
   vectorc&        Y              // result vector Y
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::BlasL2GeMV(
   ENUM_BLAS_TRANS trans,         // specifies option op(A)
   complexf        alpha,         // scalar multiplier alpha
   vectorcf&       X,             // vector X
   complexf        beta,          // scalar multiplier beta
   vectorcf&       Y              // result vector Y
   );

```

Parameters

trans

[in]  Value from the ENUM_BLAS_TRANS enumeration, which specifies the operation:

if trans= 'N', then y = alpha * A * x + beta * y;

if trans= 'T', then y = alpha * A**T * x + beta * y;

if trans= 'C', then y = alpha * A**H * x + beta * y.

alpha

[in]  Scalar multiplier alpha.

X

[in]  Vector x of size n if trans='N', or of size m otherwise.

beta

[in]  Scalar multiplier beta.

Y

[in, out]  Result vector y of size m if trans='N', or of size n otherwise. If beta is not zero, then vector Y should contain actual data before entry.If vector size differs from actual, then vector Y will be resized and zeroed.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

ENUM_BLAS_TRANS

An enumeration defining option op(A).

| ID | Description |
| --- | --- |
| BLASTRANS_N | 'N': No transpose |
| BLASTRANS_T | 'T': Transpose |
| BLASTRANS_C | 'C': Conjugate transpose |
