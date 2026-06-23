# SingularValueDecompositionBidiagDC

Singular Value Decomposition, divide-and-conquer algorithm for bidiagonal matrices (LAPACK function [BDSDC](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/bdsdc.html)).

Computing for type matrix<double>

```
bool  matrix::SingularValueDecompositionBidiagDC(
   ENUM_SVDBIDIAG_Z    jobz,       // how to compute singular vectors
   vector&             S,          // vector of computed singular values
   matrix&             U,          // U matrix of computed left vectors
   matrix&             VT          // VT transposed matrix of right vectors
   );

```

Computing for type matrix<float>

```
bool  matrixf::SingularValueDecompositionBidiagDC(
   ENUM_SVDBIDIAG_Z    jobz,       // how to compute singular vectors
   vectorf&            S,          // vector of computed singular values
   matrixf&            U,          // U matrix of computed left vectors
   matrixf&            VT          // VT transposed matrix of right vectors
   );

```

Parameters

jobz

[in]  [ENUM_SVDBIDIAG_Z](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondddc#enum_svdbidiag_z) enumeration value that determines how the singular vectors should be computed.

S

[out] Vector of singular values.

U

[out] Matrix of left singular vectors.

VT

[out] Transposed matrix of right singular vectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Computation depends on the values of the jobz and range parameters.

A bidiagonal matrix is a square matrix with non-zero main diagonal and one of the sub-diagonals.

Upper bidiagonal matrix

```
[[x, x, 0, 0, 0],
 [0, x, x, 0, 0],
 [0, 0, x, x, 0],
 [0, 0, 0, x, x],
 [0, 0, 0, 0, x]]

```

Lower bidiagonal matrix

```
[[x, 0, 0, 0, 0],
 [x, x, 0, 0, 0],
 [0, x, x, 0, 0],
 [0, 0, x, x, 0],
 [0, 0, 0, x, x]]

```

ENUM_SVDBIDIAG_Z

An enumeration defining how left singular vectors should be computed.

| ID | Description |
| --- | --- |
| SVDJOBZ_V | Compute singular values and singular vectors. |
| SVDJOBZ_N | Compute singular values only. |

See also

[SingularValueDecompositionDC](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondc), [SingularValueDecompositionQR](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqr)
