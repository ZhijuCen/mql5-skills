# BlasL3LARCM

Multiplies a square real matrix by a complex matrix.

C = A * B

where A is m-by-m and real; B is m-by-n and complex; C is m-by-n and complex.

BLAS function [LARCM](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2026-0/larcm.html).

Computing for type matrix<double>

```
bool  matrix::BlasL3LARCM(
   matrixc&        B,             // matrix B
   matrixc&        C              // result matrix C
   );

```

Computing for type matrix<float>

```
bool  matrixf::BlasL3LARCM(
   matrixcf&       B,             // matrix B
   matrixcf&       C              // result matrix C
   );

```

Parameters

B

[in]  Complex matrix B of size m-by-n.

C

[out]  Result complex matrix C of size m-by-n.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
