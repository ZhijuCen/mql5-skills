# BlasL3LACRM

Multiplies a complex matrix by a square real matrix.

C = A * B

where A is m-by-n and complex; B is n-by-n and real; C is m-by-n and complex.

BLAS function [LACRM](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2026-0/lacrm.html).

Computing for type matrix<complex>

```
bool  matrixc::BlasL3LACRM(
   matrix&         B,             // matrix B
   matrixc&        C              // result matrix C
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::BlasL3LACRM(
   matrixf&        B,             // matrix B
   matrixcf&       C              // result matrix C
   );

```

Parameters

B

[in]  Real matrix B of size n-by-n.

C

[out]  Result complex matrix C of size m-by-n.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
