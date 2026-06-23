# SingularValueDecompositionBidiagQR

Computes the singular value decomposition of a general matrix that has been reduced to bidiagonal form by the method [ReduceToBidiagonal](/en/docs/matrix/openblas/matrixtransforms/reducetobidiagonal). LAPACK function [BDSQR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-0/bdsqr.html).

Computing for type matrix<double>

```
bool  matrix::SingularValueDecompositionBidiagQR(
   matrix&         Q,        // orthogonal matrix Q
   matrix&         PT,       // transposed matrix P
   vector&         S,        // vector of computed singular values
   matrix&         U,        // matrix U of computed left vectors
   matrix&         VT        // transposed matrix V of right vectors
   );

```

Computing for type matrix<float>

```
bool  matrixf::SingularValueDecompositionBidiagQR(
   matrix&         Q,        // orthogonal matrix Q
   matrix&         PT,       // transposed matrix P
   vectorf&        S,        // vector of computed singular values
   matrixf&        U,        // matrix U of computed left vectors
   matrixf&        VT        // transposed matrix V of right vectors
   );

```

Computing for type matrix<complex>

```
bool  matrixc::SingularValueDecompositionBidiagQR(
   matrix&         Q,        // orthogonal matrix Q
   matrix&         PH,       // Hermitian conjugated matrix P
   vector          S,        // vector of computed singular values
   matrixc         U,        // matrix U of computed left vectors
   matrixc         VH        // Hermitian conjugated matrix V of right vectors
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::SingularValueDecompositionBidiagQR(
   matrixf&        Q,        // orthogonal matrix Q
   matrixf&        PH,       // Hermitian conjugated matrix P
   vectorf&        S,        // vector of computed singular values
   matrixcf&       U,        // matrix U of computed left vectors
   matrixcf&       VH        // Hermitian conjugated matrix V of right vectors
   );

```

Parameters

Q

[in]  Orthogonal matrix Q produced by method [ReflectBidiagonalToQP](/en/docs/matrix/openblas/matrixtransforms/reflectbidiagonaltoqp). If matrix Q has zero size, then left vectors U are not calculated.

PT

[in]  Transposed (or hermitian conjugated) matrix P produced by method [ReflectBidiagonalToQP](/en/docs/matrix/openblas/matrixtransforms/reflectbidiagonaltoqp). If matrix PT has zero size, then right vectors VT are not calculated.

S

[out] Vector of singular values.

U

[out] Matrix of left singular vectors.

VT

[out] Matrix of right singular vectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

BDSQR computes the singular values and, optionally, the right and/or left singular vectors from the singular value decomposition (SVD) of a N-by-N (upper or lower) bidiagonal matrix B using the implicit zero-shift QR algorithm.  The SVD of B has the form

B = Q * S * P**T

where S is the diagonal matrix of singular values, Q is an orthogonal matrix of left singular vectors, and P is an orthogonal matrix of right singular vectors.  If left singular vectors are requested, this subroutine actually returns U*Q instead of Q, and, if right singular vectors are requested, this subroutine returns P**T*VT instead of P**T, for given real input matrices U and VT.  When U and VT are the orthogonal matrices that reduce a general matrix A to bidiagonal form:  A = U*B*VT, as computed by GEBRD, then

A = (U*Q) * S * (P**T*VT)

is the SVD of A.
