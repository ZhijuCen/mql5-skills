# FactorizationLDLSyTridPD

Forms the factorization of a symmetric positive-definite or, for complex data, Hermitian positive-definite tridiagonal matrix A:

A = L * D * L**T in case of lower triangular or symmetric matrix A

or

A = U**T * D * U in case of upper triangular matrix A

where L is lower triangular with unit diagonal elements, U is upper triangular with unit diagonal elements. D is diagonal matrix. LAPACK function [PTTRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/pttrf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationLDLSyTridPD(
   matrix&         L,            // lower or upper triangular matrix
   matrix&         D             // diagonal matrix D
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationLDLSyTridPD(
   matrixf&        L,            // lower or upper triangular matrix
   matrixf&        D             // diagonal matrix D
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationLDLSyTridPD(
   matrixc&        L,            // lower or upper triangular matrix
   matrixc&        D             // diagonal matrix D
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationLDLSyTridPD(
   matrixcf&       L,            // lower or upper triangular matrix
   matrixcf&       D             // diagonal matrix D
   );

```

Parameters

L

[out]  Lower or upper triangular matrix with unit diagonal elements.

D

[out]  Diagonal matrix D.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Matrices L and D can be used for further calculations with methods [LDLSyTridPDLinearEquationsSolution](/en/docs/matrix/openblas/factored_calculations/ldlsytridpdlinearequations) and [LDLSyTridPDCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/ldlsytridpdcondnumreciprocal).
