# FactorizationPLUQ

Computes an LU factorization of a general N-by-N matrix A with complete pivoting (row and column interchanges). The factorization has the form

A = P * L * U * Q

where P is a rows permutation matrix, L is lower triangular with unit diagonal elements, U is upper triangular, and Q is a columns permutation matrix. LAPACK function [GETC2](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/getc2.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationPLUQ(
   matrix&         P,            // rows permutation matrix P
   matrix&         L,            // lower triangular matrix L
   matrix&         U,            // upper triangular matrix U
   matrix&         Q             // cols permutation matrix Q
   );

```

Computing for type matrix<float>

```
bool  matrixf::FactorizationPLUQ(
   matrixf&        P,            // rows permutation matrix P
   matrixf&        L,            // lower triangular matrix L
   matrixf&        U,            // upper triangular matrix U
   matrixf&        Q             // cols permutation matrix Q
   );

```

Computing for type matrix<complex>

```
bool  matrixc::FactorizationPLUQ(
   matrixc&        P,            // rows permutation matrix P
   matrixc&        L,            // lower triangular matrix L
   matrixc&        U,            // upper triangular matrix U
   matrixc&        Q             // cols permutation matrix Q
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::FactorizationPLUQ(
   matrixcf&       P,            // rows permutation matrix P
   matrixcf&       L,            // lower triangular matrix L
   matrixcf&       U,            // upper triangular matrix U
   matrixcf&       Q             // cols permutation matrix Q
   );

```

Parameters

P

[out]  Rows permutation matrix P.

L

[out]  Lower triangular matrix L with unit diagonal elements.

U

[out]  Upper triangular matrix U.

Q

[out]  Cols permutation matrix Q.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).
