# SingularValueDecompositionQR

Singular Value Decomposition, QR algorithm. Considered a classical SVD algorithm (LAPACK function [GESVD](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gesvd.html)).

Computing for type matrix<double>

```
bool  matrix::SingularValueDecompositionQR(
   ENUM_SVD_Z      jobu,     // how to compute left vectors
   ENUM_SVD_Z      jobv,     // how to compute right vectors
   vector&         S,        // vector of computed singular values
   matrix&         U,        // matrix of computed left vectors U
   matrix&         VT        // transposed matrix of right vectors VT
   );

```

Computing for type matrix<float>

```
bool  matrixf::SingularValueDecompositionQR(
   ENUM_SVD_Z      jobu,     // how to compute left vectors
   ENUM_SVD_Z      jobv,     // how to compute right vectors
   vectorf&        S,        // vector of computed singular values
   matrixf&        U,        // matrix of computed left vectors U
   matrixf&        VT        // transposed matrix of right vectors VT
   );

```

Computing for type matrix<complex>

```
bool  matrixc::SingularValueDecompositionQR(
   ENUM_SVD_Z      jobu,     // how to compute left vectors
   ENUM_SVD_Z      jobv,     // how to compute right vectors
   vector          S,        // vector of computed singular values
   matrixc         U,        // matrix of computed left vectors U
   matrixc         VT        // transposed matrix of right vectors VT
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::SingularValueDecompositionQR(
   ENUM_SVD_Z      jobu,                   // how to compute left vectors
   ENUM_SVD_Z      jobv,                   // how to compute right vectors
   vectorf&        singular_values,        // vector of computed singular values
   matrixcf&       u,                      // matrix of computed left vectors U
   matrixcf&       vt                      // transposed matrix of right vectors VT
   );

```

Parameters

jobu

[in]  [ENUM_SVD_Z](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondc#enum_svd_z) enumeration value defining how the left singular vectors should be computed.

jobv

[in]  [ENUM_SVD_Z](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondc#enum_svd_z) enumeration value defining how the right singular vectors should be computed.

S

[out] Vector of singular values.

U

[out] Matrix of left singular vectors.

VT

[out] Matrix of right singular vectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Computation depends on the value of the jobu and jobv parameters.

When set to SVDZ_N, the left (jobu) and right (jobv) vectors are not computed. Singular values are always computed.

When set to SVDZ_A, the full matrices of vectors U (jobu) or VT (jobv) are computed.

With the value SVDZ_S, truncated matrices of vectors U (jobu) or VT (jobv) are computed.

ENUM_SVD_Z

An enumeration defining the way to compute left and right singular vectors.

| ID | Description |
| --- | --- |
| SVDZ_N | Columns U or rows VT are not computed |
| SVDZ_A | All M columns of U or all N columns of VT are returned in arrays U and VT |
| SVDZ_S | The first min(M,N) columns of U or the first min(M,N) columns of VT are returned in arrays U and VT |

See also

[SingularValueDecompositionDC](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondc), [SingularValueDecompositionQRPivot](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqrp)
