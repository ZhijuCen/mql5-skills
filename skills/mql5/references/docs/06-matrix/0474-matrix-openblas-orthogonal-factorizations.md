# Orthogonal Factorizations

OpenBLAS provides a set of routines for factoring a general (m \times n) rectangular matrix (A) into the product of an orthogonal (unitary in the complex case) matrix and a triangular (or, in some cases, trapezoidal) matrix.

A real matrix (Q) is called orthogonal if (Q^TQ = I), while a complex matrix (Q) is called unitary if (Q^HQ = I). Orthogonal and unitary matrices have the important property of preserving the Euclidean norm of a vector::

||x||2 = ||Qx||2, whenever (Q) is orthogonal or unitary.

As a result, these matrices contribute to numerical stability, since they do not amplify rounding errors.

Orthogonal factorizations are widely used for solving least-squares problems. They can also be employed as preprocessing steps in the solution of eigenvalue and singular value problems.

| Функция | Выполняемое действие |
| --- | --- |
| FactorizationQR | Computes the QR factorization of a general m-by-n matrix: A = Q * R. LAPACK function  GEQRF . |
| FactorizationQRNonNeg | Computes the QR factorization of a general m-by-n matrix: A = Q * R. R is an upper triangular matrix with nonnegative diagonal entries. LAPACK function  GEQRFP . |
| FactorizationQRPivot | Computes the QR factorization of a general m-by-n matrix with column pivoting: A * P = Q * R. LAPACK function  GEQP3 . |
| FactorizationQRTallSkinny | Computes a blocked Tall-Skinny QR factorization of an m-by-n (m>n) matrix: A = Q * R. LAPACK function  LATSQR . |
| FactorizationLQ | Computes the LQ factorization of a general m-by-n matrix: A = L * Q. LAPACK function  GELQF . |
| FactorizationLQShortWide | Computes a blocked Short-Wide LQ factorization of an m-by-n (m<n) matrix: A = L * Q. LAPACK function  LASWLQ . |
| FactorizationQL | Computes the QL factorization of a general m-by-n matrix: A = Q * L. LAPACK function  GEQLF . |
| FactorizationRQ | Computes the RQ factorization of a general m-by-n matrix: A = R * Q. LAPACK function  GERQF . |
| FactorizationRZ | Reduces the M-by-N ( M<=N ) real or complex upper trapezoidal matrix A to upper triangular form by means of orthogonal transformations. LAPACK function  TZRZF . |
| FactorizationQR2 | Computes the generalized QR factorization of two matrices - A of n-by-m size and B of n-by-p size: A = Q * R, B = Q * T * Z. LAPACK function  GGQRF . |
| FactorizationRQ2 | Computes the generalized RQ factorization of an m-by-n matrix A and a p-by-n matrix B: A = R * Q, B = Z * T * Q. 
 LAPACK function  GGRQF . |
