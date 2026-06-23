# FactorizationLDLComplexSy

Computes the factorization of a complex symmetric (not Hermitian conjugated!) matrix A using the Bunch-Kaufman diagonal pivoting method. The form of the factorization is:

A = L * D * L**T in case of lower triangular or symmetric matrix A

or

A = U * D * U**T in case of upper triangular matrix A

where L is lower triangular with unit diagonal elements, U is upper triangular with unit diagonal elements. D is a symmetric block-diagonal matrix with 1-by-1 and 2-by-2 diagonal blocks. LAPACK function [SYTRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/sytrf.html).

Computing for type matrix<complex>

```
bool  matrix::FactorizationLDLComplexSy(
   matrixc&        L,            // lower or upper triangular matrix
   matrixc&        D             // diagonal matrix D
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationLDLComplexSy(
   matrixcf&       L,            // lower or upper triangular matrix
   matrixcf&       D             // diagonal matrix D
   );

```

Parameters

L

[out]  Lower or upper triangular matrix with unit diagonal elements.

D

[out]  Symmetric block-diagonal matrix D.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The input can be a complex symmetric, [upper triangular](/en/docs/matrix/matrix_manipulations/matrix_triu) or [lower triangular](/en/docs/matrix/matrix_manipulations/matrix_tril) matrix. Triangular matrices are assumed to be complex symmetric.

As a result of the computations, the lower-triangular matrix L (or the upper-triangular matrix U) may become permuted.
