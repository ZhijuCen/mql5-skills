# SingularValueDecompositionDC

Singular Value Decomposition, "divide-and-conquer" algorithm. This algorithm is considered the fastest among other SVD algorithms (LAPACK function [GESDD](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gesdd.html)).

Computing for type matrix<double>

```
bool  matrix::SingularValueDecompositionDC(
   ENUM_SVD_Z      jobz,     // how to computed
   vector&         S,        // vector of computed singular values
   matrix&         U,        // matrix of computed left vectors U
   matrix&         VT        // transposed matrix of right vectors VT
   );

```

Computing for type matrix<float>

```
bool  matrixf::SingularValueDecompositionDC(
   ENUM_SVD_Z      jobz,     // how to computed
   vectorf&        S,        // vector of computed singular values
   matrixf&        U,        // matrix of computed left vectors U
   matrixf&        VT        // transposed matrix of right vectors VT
   );

```

Computing for type matrix<complex>

```
bool  matrixc::SingularValueDecompositionDC(
   ENUM_SVD_Z      jobz,     // how to computed
   vector&         S,        // vector of computed singular values
   matrixc&        U,        // matrix of computed left vectors U
   matrixc&        VT        // transposed matrix of right vectors VT
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::SingularValueDecompositionDC(
   ENUM_SVD_Z      jobz,                   // how to computed
   vectorf&        singular_values,        // vector of computed singular values
   matrixcf&       U,                      // matrix of computed left vectors U
   matrixcf&       VT                      // transposed matrix of right vectors VT
   );

```

Parameters

jobz

[in]  [ENUM_SVD_Z](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondc#enum_svd_z) enumeration value which determines the method for computing left and singular eigenvectors.

S

[out] Vector of singular values.

U

[out] Matrix of left singular vectors.

VT

[out] Matrix of right singular vectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Computation depends on the value of the jobz parameter.

When jobv is set to SVDZ_N, the left and right vectors are not computed. Only singular values are computed.

When jobv is set to SVDZ_A, the full matrices of the U and VT vectors are computed.

When the value is SVDZ_S, truncated matrices of vectors U and VT are computed.

ENUM_SVD_Z

An enumeration defining the way to compute left and right singular vectors.

| ID | Description |
| --- | --- |
| SVDZ_N | Columns U or rows VT are not computed |
| SVDZ_A | All M columns of U or all N columns of VT are returned in arrays U and VT |
| SVDZ_S | The first min(M,N) columns of U or the first min(M,N) columns of VT are returned in arrays U and VT |

See also

[SingularValueDecompositionQR](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqr), [SingularValueDecompositionQRPivot](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqrp)
