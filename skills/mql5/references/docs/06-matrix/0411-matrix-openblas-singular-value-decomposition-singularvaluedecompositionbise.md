# SingularValueDecompositionBisection

Singular Value Decomposition, bisection algorithm (LAPACK function [GESVDX](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gesvdx.html)).

Computing for type matrix<double>

```
bool  matrix::SingularValueDecompositionBisection(
   ENUM_SVD_VECTORS    jobv,     // compute left and right singular vectors
   ENUM_BLAS_RANGE     range,    // subset of computable singular values
   double              lower,    // lower limit of the subset
   double              upper,    // upper limit of the subset
   vector&             S,        // vector of computed singular values
   matrix&             U,        // matrix of computed left vectors U
   matrix&             VT        // transposed matrix of right vectors VT
   );

```

Computing for type matrix<float>

```
bool  matrixf::SingularValueDecompositionBisection(
   ENUM_SVD_VECTORS    jobv,     // compute left and right singular vectors
   ENUM_BLAS_RANGE     range,    // subset of computable singular values
   double              lower,    // lower limit of the subset
   double              upper,    // upper limit of the subset
   vectorf&            S,        // vector of computed singular values
   matrixf&            U,        // matrix of computed left vectors U
   matrixf&            VT        // ransposed matrix of right vectors VT
   );

```

Computing for type matrix<complex>

```
bool  matrixc::SingularValueDecompositionBisection(
   ENUM_SVD_VECTORS    jobv,     // compute left and right singular vectors
   ENUM_BLAS_RANGE     range,    // subset of computable singular values
   double              lower,    // lower limit of the subset
   double              upper,    // upper limit of the subset
   vector              S,        // vector of computed singular values
   matrixc             U,        // matrix of computed left vectors U
   matrixc             VT        // transposed matrix of right vectors VT
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::SingularValueDecompositionBisection(
   ENUM_SVD_VECTORS    jobv,     // compute left and right singular vectors
   ENUM_BLAS_RANGE     range,    // subset of computable singular values
   double              lower,    // lower limit of the subset
   double              upper,    // upper limit of the subset
   vectorf&            S,        // vector of computed singular values
   matrixcf&           U,        // matrix of computed left vectors U
   matrixcf&           VT        // transposed matrix of right vectors VT
   );

```

Parameters

jobv

[in]  ENUM_SVD_VECTORS enumeration value which determines the method for computing left and right singular vectors.

range

[in]  ENUM_BLAS_RANGE enumeration value that defines a subset of computable singular values and vectors.

lower

[in]  The lower limit of singular values subset; specified depending on the value of the range parameter.

upper

[in]  The upper limit of singular values subset; specified depending on the value of the range parameter.

S

[out] Vector of singular values.

U

[out] Matrix of left singular vectors.

VT

[out] Matrix of right singular vectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Computation depends on the values of the jobuv and range parameters.

When BLASRANGE_A is set, all singular values are computed, and the lower and upper parameters are ignored.

With the BLASRANGE_V value, only those singular values (and their vectors) that fall within the range of real values specified by the 'lower' and 'upper' parameters are computed.

With the BLASRANGE_I value, only those singular values (and their vectors) that fall within the range of integer indices specified by the 'lower' and 'upper' parameters are computed. For example, with lower=0 and upper=2, only the first three singular values are computed.

ENUM_SVD_VECTORS

An enumeration defining the way to compute left and right singular vectors.

| ID | Description |
| --- | --- |
| SVDVECTORS_N | Only singular values are computed, without vectors. |
| SVDVECTORS_U | Left singular vectors are computed. |
| SVDVECTORS_V | Right singular vectors are computed. |
| SVDVECTORS_UV | Left and right singular vectors are computed. |

ENUM_BLAS_RANGE

An enumeration defining a subset of computable singular values and vectors.

| ID | Description |
| --- | --- |
| BLASRANGE_A | All singular or eigenvalues will be found. |
| BLASRANGE_V | All singular or eigenvalues in the half-open interval (VL,VU] will be found. |
| BLASRANGE_I | Singular or eigenvalues from IL to IU will be found |

See also

[SingularValueDecompositionDC](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondc), [SingularValueDecompositionQR](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqr), [SingularValueDecompositionQRPivot](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqrp)
