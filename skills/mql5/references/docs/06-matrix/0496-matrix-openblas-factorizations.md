# Factorizations

The Factorizations section contains functions for performing various types of matrix factorizations used in numerical solutions of linear systems, stability analysis, and other linear algebra tasks. These factorizations transform the original matrix into simpler forms, making subsequent computations more efficient. All functions are implemented using LAPACK routines and support the types [double](/en/docs/basis/types/double), float, [complex](/en/docs/basis/types/complex), and complexf.

The functions in this section are used for:

- Preprocessing matrices when solving systems of linear equations;
- Computing determinants, ranks, and matrix inverses;
- Assessing the stability of numerical methods;
- Solving problems in spectral theory and optimization methods.

Matrix factorization is a critical step in many linear algebra algorithms, and this section provides access to the most efficient and well-established factorization techniques.

| Function | Action |
| --- | --- |
| FactorizationPLU | Computes an LU factorization of a general M-by-N matrix A using partial pivoting with row interchanges. The factorization has the form A = P * L * U. LAPACK function  GETRF . |
| FactorizationPLUQ | Computes an LU factorization of a general N-by-N matrix A with complete pivoting (row and column interchanges). The factorization has the form A = P * L * U * Q where P is a rows permutation matrix, L is lower triangular with unit diagonal elements, U is upper triangular, and Q is a columns permutation matrix. LAPACK function  GETC2 . |
| FactorizationPLUGeTrid | Computes an LU factorization of a general (non-symmetric) tridiagonal N-by-N matrix A using elimination with partial pivoting and row interchanges. The factorization has the form A = P * L * U. LAPACK function  GTTRF . |
| FactorizationLDL | Computes the factorization of a real symmetric or complex Hermitian matrix A using the Bunch-Kaufman diagonal pivoting method. LAPACK functions  SYTRF ,  HETRF . |
| FactorizationLDLComplexSy | Computes the factorization of a complex symmetric (not Hermitian conjugated!) matrix A using the Bunch-Kaufman diagonal pivoting method. LAPACK function  SYTRF . |
| FactorizationLDLSyTridPD | Forms the factorization of a symmetric positive-definite or, for complex data, Hermitian positive-definite tridiagonal matrix A. LAPACK function  PTTRF . |
| FactorizationCholesky | Computes the factorization of a real symmetric or complex Hermitian positive-definite matrix A.  LAPACK function  POTRF . |
| FactorizationCholeskySyPS | Computes the Cholesky factorization with complete pivoting of a real symmetric (complex Hermitian) positive semidefinite N-by-N matrix. LAPACK function  PSTRF . |
| FactorizationPLURaw | Computes an LU factorization of a general M-by-N matrix A using partial pivoting with row interchanges. The factorization has the form A = P * L * U where P is a permutation matrix, L is lower triangular with unit diagonal elements (lower trapezoidal if m > n), and U is upper triangular (upper trapezoidal if m < n). LAPACK function  GETRF . |
| FactorizationPLUQRaw | Computes an LU factorization of a general N-by-N matrix A with complete pivoting (row and column interchanges). The factorization has the form A = P * L * U * Q where P is a rows permutation matrix, L is lower triangular with unit diagonal elements, U is upper triangular, and Q is a columns permutation matrix. LAPACK function  GETC2 . |
| FactorizationPLUGeTridRaw | Computes an LU factorization of a general (non-symmetric) tridiagonal N-by-N matrix A using elimination with partial pivoting and row interchanges. The factorization has the form A = P * L * U where P is a permutation matrix, L is lower triangular with unit diagonal elements, and U is upper triangular. LAPACK function  GTTRF . |
| FactorizationLDLRaw | Computes the factorization of a real symmetric or complex Hermitian matrix A using the Bunch-Kaufman diagonal pivoting method. LAPACK functions  SYTRF ,  HETRF . |
| FactorizationLDLComplexSyRaw | Computes the factorization of a complex symmetric matrix A using the Bunch-Kaufman diagonal pivoting method. LAPACK function  SYTRF . |
