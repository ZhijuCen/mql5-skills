# FactorizationCholeskySyPS

Computes the Cholesky factorization with complete pivoting of a real symmetric (complex Hermitian) positive semidefinite N-by-N matrix. The form of the factorization is:

P**T * A * P = L *  L**T in case of lower triangular or symmetric matrix A

or

P**T * A * P = U**T  * U in case of upper triangular matrix A

where P is a permutation matrix, L is lower triangular, U is upper triangular. LAPACK function [PSTRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/pstrf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationCholeskySyPS(
   double          tol           // tolerance
   matrix&         P,            // permutation matrix P
   matrix&         L             // lower or upper triangular matrix
   );

```

Computing for type matrix<float>

```
bool  matrix::FactorizationCholeskySyPS(
   float           tol           // tolerance
   matrixf&        P,            // permutation matrix P
   matrixf&        L             // lower or upper triangular matrix
   );

```

Computing for type matrix<complex>

```
bool  matrix::FactorizationCholeskySyPS(
   double          tol           // tolerance
   matrixc&        P,            // permutation matrix P
   matrixc&        L             // lower or upper triangular matrix
   );

```

Computing for type matrix<complexf>

```
bool  matrix::FactorizationCholeskySyPS(
   float           tol           // tolerance
   matrixcf&       P,            // permutation matrix P
   matrixcf&       L             // lower or upper triangular matrix
   );

```

Parameters

tol

[in]  User defined tolerance. If tol < 0, then n*ε*max(A[k,k]), where ε is the machine precision, will be used. The algorithm terminates at the (k-1)st step, if the pivot <=tol.

P

[out]  Permutation matrix P.

L

[out]  Lower or upper triangular matrix.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The input can be a symmetric (Hermitian), [upper triangular](/en/docs/matrix/matrix_manipulations/matrix_triu) or [lower triangular](/en/docs/matrix/matrix_manipulations/matrix_tril) matrix. Triangular matrices are assumed to be symmetric (Hermitian conjugated).
