# SingularValueDecompositionJacobiLow

Singular Value Decomposition, Jacobi low level algorithm (LAPACK function [GESVJ](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gesvj.html)). The method computes small singular values and their singular vectors with much greater accuracy than other SVD routines in certain cases.

Computing for type matrix<double>

```
bool  matrix::SingularValueDecompositionJacobiLow(
   ENUM_SVDJH_U   jobu,            // how to compute left vectors
   ENUM_SVDJH_V   jobv,            // how to compute right vectors
   double         ctol,            // threshold for convergence if jobu='C'
   ulong          mv,              // number of first rows of matrix V if jobv='A'
   vector&        S,               // vector of computed singular values
   matrix&        U,               // matrix of computed left vectors U
   matrix&        V,               // matrix of computed left vectors V
   vector&        work_results     // additional computation results
   );

```

Computing for type matrix<float>

```
bool  matrixf::SingularValueDecompositionJacobiLow(
   ENUM_SVDJH_U   jobu,            // how to compute left vectors
   ENUM_SVDJH_V   jobv,            // how to compute right vectors
   double         ctol,            // threshold for convergence if jobu='C'
   ulong          mv,              // number of first rows of matrix V if jobv='A'
   vectorf&       S,               // vector of computed singular values
   matrixf&       U,               // U matrix of computed left vectors
   matrixf&       V,               // V matrix of computed left vectors
   vector&        work_results     // additional computation results
   );

```

Computing for type matrix<complex>

```
bool  matrixc::SingularValueDecompositionJacobiLow(
   ENUM_SVDJH_U   jobu,            // how to compute left vectors
   ENUM_SVDJH_V   jobv,            // how to compute right vectors
   double         ctol,            // threshold for convergence if jobu='C'
   ulong          mv,              // number of first rows of matrix V if jobv='A'
   vector&        S,               // vector of computed singular values
   matrixc&       U,               // U matrix of computed left vectors
   matrixc&       V,               // V matrix of computed left vectors
   vector&        work_results     // additional computation results
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::SingularValueDecompositionJacobiLow(
   ENUM_SVDJH_U    jobu,                   // how to compute left vectors
   ENUM_SVDJH_V    jobv,                   // how to compute right vectors
   double          ctol,                   // threshold for convergence if jobu='C'
   ulong           mv,                     // number of first rows of matrix V if jobv='A'
   vectorf&        singular_values,        // vector of computed singular values S
   matrixcf&       u,                      // matrix of computed left vectors U
   matrixcf&       v,                      // matrix of computed left vectors V
   vectorf&        work_results            // additional computation results
   );

```

Parameters

jobu

[in]  [ENUM_SVDJL_U](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionjl#enum_svdjl_u) enumeration value that determines how the left singular vectors should be computed.

jobv

[in]  [ENUM_SVDJL_V](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionjl#enum_svdjl_v) enumeration value defining how the right singular vectors should be computed.

ctol

[in] Convergence threshold if jobu=SVDJLU_C. For other values of 'jobu' the parameter is ignored.

mv

[in] Number of rows of matrix V to be computed if jobv=SVDJLV_A. For other values of 'jobv' the parameter is ignored.

S

[out] Vector of singular values.

Depending on the value scale = work(1), where scale is the scaling factor:

if scale = 1, S(1:n) contains the computed singular values of a. During the computation, sva contains the Euclidean column norms of the iterated matrices in the array a.

if scale ≠ 1, the singular values of a are scale*S(1:n), and this factored representation is due to the fact that some of the singular values of a might underflow or overflow.

U

[out] Matrix of left singular vectors.

V

[out] Matrix of right singular vectors (non-transposed).

work_results

[out] Vector consisting of 7 statistics obtained as a result of the computation.

work(1) = scale is the scaling factor such that scale*S(1:n) are the computed singular values of A. See the description of S).

work(2) is the number of the computed nonzero singular value.

work(3) is the number of the computed singular values that are larger than the underflow threshold.

work(4) is the number of sweeps of Jacobi rotations needed for numerical convergence.

work(5) = max_{i.NE.j} |COS(A(:,i),A(:,j))| in the last sweep. This is useful information in cases when ?gesvj did not converge, as it can be used to estimate whether the output is still useful and for post festum analysis.

work(6) is the largest absolute value over all sines of the Jacobi rotation angles in the last sweep. It can be useful in a post festum analysis.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The number of matrix rows must not be less than the number of columns.

ENUM_SVDJL_U

An enumeration defining how left singular vectors should be computed.

| ID | Description |
| --- | --- |
| SVDJLU_U | The left singular vectors corresponding to the nonzero singular values are computed and returned in the leading columns of A |
| SVDJLU_C | Analogous to SVDJLU_U, except that user can control the level of numerical orthogonality of the computed left singular vectors. |
| SVDJLU_N | The matrix U is not computed. |

ENUM_SVDJL_V

An enumeration defining how right singular vectors should be computed.

| ID | Description |
| --- | --- |
| SVDJLV_V | The matrix V is computed |
| SVDJLV_A | The Jacobi rotations are applied to the MV-by-N matrix V. |
| SVDJLV_N | The matrix V is not computed. |

See also

[SingularValueDecompositionDC](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondc), [SingularValueDecompositionQR](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqr)
