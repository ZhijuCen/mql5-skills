# SingularValueDecompositionJacobiHigh

Singular Value Decomposition, Jacobi high level algorithm (LAPACK function [GEJSV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gejsv.html)).

Computing for type matrix<double>

```
bool  matrix::SingularValueDecompositionJacobiHigh(
   ENUM_SVDJH_A   joba,            // computation accuracy level
   ENUM_SVDJH_U   jobu,            // how to compute left vectors
   ENUM_SVDJH_V   jobv,            // how to compute right vectors
   ENUM_SVDJH_R   jobr,            // define range of computable singular values
   ENUM_SVDJH_T   jobt,            // define whether to transpose when computing a square matrix
   ENUM_SVDJH_P   jobp,            // the possibility of structured perturbations to remove denormalized values
   vector&        S,               // vector of computed singular values
   matrix&        U,               // matrix of computed left vectors U
   matrix&        V,               // matrix of computed left vectors V
   vector&        work_results     // additional computation results
   );

```

Computing for type matrix<float>

```
bool  matrixf::SingularValueDecompositionJacobiHigh(
   ENUM_SVDJH_A   joba,            // computation accuracy level
   ENUM_SVDJH_U   jobu,            // how to compute left vectors
   ENUM_SVDJH_V   jobv,            // how to compute right vectors
   ENUM_SVDJH_R   jobr,            // define range of computable singular values
   ENUM_SVDJH_T   jobt,            // define whether to transpose when computing a square matrix
   ENUM_SVDJH_P   jobp,            // the possibility of structured perturbations to remove denormalized values
   vectorf&       S,               // vector of computed singular values
   matrixf&       U,               // U matrix of computed left vectors
   matrixf&       V,               // V matrix of computed left vectors
   vector&        work_results     // additional computation results
   );

```

Computing for type matrix<complex>

```
bool  matrixc::SingularValueDecompositionJacobiHigh(
   ENUM_SVDJH_A   joba,            // computation accuracy level
   ENUM_SVDJH_U   jobu,            // how to compute left vectors
   ENUM_SVDJH_V   jobv,            // how to compute right vectors
   ENUM_SVDJH_R   jobr,            // define range of computable singular values
   ENUM_SVDJH_T   jobt,            // define whether to transpose when computing a square matrix
   ENUM_SVDJH_P   jobp,            // the possibility of structured perturbations to remove denormalized values
   vectorc&       S,               // vector of computed singular values
   matrixc&       U,               // U matrix of computed left vectors
   matrixc&       V,               // V matrix of computed left vectors
   vector&        work_results     // additional computation results
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::SingularValueDecompositionJacobiHigh(
   ENUM_SVDJH_A    joba,                   // computation accuracy level
   ENUM_SVDJH_U    jobu,                   // how to compute left vectors
   ENUM_SVDJH_V    jobv,                   // how to compute right vectors
   ENUM_SVDJH_R    jobr,                   // define range of computable singular values
   ENUM_SVDJH_T    jobt,                   // define whether to transpose when computing a square matrix
   ENUM_SVDJH_P    jobp,                   // the possibility of structured perturbations to remove denormalized values
   vectorf&        singular_values,        // vector of computed singular values S
   matrixcf&       u,                      // matrix of computed left vectors U
   matrixcf&       v,                      // matrix of computed left vectors V
   vectorf&        work_results            // additional computation results
   );

```

Parameters

joba

[in]  [ENUM_SVDJH_A](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionjh#enum_svdjh_a) enumeration value determining the accuracy level of the SVD computation.

jobu

[in]  [ENUM_SVDJH_U](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionjh#enum_svdjh_u) enumeration value that determines how the left singular vectors should be computed.

jobv

[in]  [ENUM_SVDJH_V](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionjh#enum_svdjh_v) enumeration value that determines how the right singular vectors should be computed.

jobr

[in]  [ENUM_SVDJH_R](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionjh#enum_svdjh_r) enumeration value defining the range of computable values

jobt

[in]  [ENUM_SVDJH_T](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionjh#enum_svdjh_t) enumeration value defining whether to transpose the matrix of it is square. If the matrix is non-square, this parameter is ignored.

jobp

[in]  [ENUM_SVDJH_P](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionjh#enum_svdjh_p) enumeration value defining the possibility of structured perturbations to remove denormalized values.

S

[out] Vector of singular values.

For work(1)/work(2) = one: the singular values of A. During the computation S contains Euclidean column norms of the iterated matrices in the array a.

For work(1)≠work(2): the singular values of A are (work(1)/work(2)) * S(1:n). This factored form is used if sigma_max(A) overflows or if small singular values have been saved from underflow by scaling the input matrix A.

jobr = 'R', some of the singular values may be returned as exact zeros obtained by 'setting to zero' because they are below the numerical rank threshold or are denormalized numbers.

U

[out] Matrix of left singular vectors.

V

[out] Matrix of right singular vectors.

work_results

[out] Vector consisting of 7 statistics obtained as a result of the computation.

work(1) = scale = work(2)/work(1) is the scaling factor such that scale*sva(1:n) are the computed singular values of A. See the description of S.

work(2) = see the description of work(1).

work(3) = sconda is an estimate for the condition number of column equilibrated A. If joba = 'E' or 'G', sconda is an estimate of sqrt(||(R**t * R)**(-1)||_1). It is computed using ?pocon. It holds n**(-1/4) * sconda ≤ ||R**(-1)||_2 ≤ n**(1/4) * sconda, where R is the triangular factor from the QRF of A. However, if R is truncated and the numerical rank is determined to be strictly smaller than n, sconda is returned as -1, indicating that the smallest singular values might be lost.

If full SVD is needed, the following two condition numbers are useful for the analysis of the algorithm. They are provied for a user who is familiar with the details of the method.

work(4) = an estimate of the scaled condition number of the triangular factor in the first QR factorization.

work(5) = an estimate of the scaled condition number of the triangular factor in the second QR factorization.

The following two parameters are computed if jobt = 'T'. They are provided for a user who is familiar with the details of the method.

work(6) = the entropy of A**t*A :: this is the Shannon entropy of diag(A**t*A) / Trace(A**t*A) taken as point in the probability simplex.

work(7) = the entropy of A*A**t.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The number of matrix rows must not be less than the number of columns.

ENUM_SVDJH_A

An enumeration that specifies the level of accuracy of the SVD computation.

| ID | Description |
| --- | --- |
| SVDJHA_C | High relative accuracy is achieved if A = B*D with well-conditioned B and arbitrary diagonal matrix D. |
| SVDJHA_E | Computation as with SVDJHA_C' with an additional estimate of the condition number. It provides a realistic error bound. |
| SVDJHA_F | Higher accuracy than the SVDJHA_C option. |
| SVDJHA_G | Computation as with SVDJHA_F with an additional estimate of the condition number. |
| SVDJHA_A | Small singular values are the noise and the matrix is treated as numerically rank deficient. |
| SVDJHA_R | Similar as in SVDJHA_A, but more accuracy. |

ENUM_SVDJH_U

An enumeration defining how left singular vectors should be computed.

| ID | Description |
| --- | --- |
| SVDJHU_U | N columns of U are returned in the array U. |
| SVDJHU_F | Full set of M left singular vectors is returned in the array U. |
| SVDJHU_N | U is not computed. |

ENUM_SVDJH_V

An enumeration defining how right singular vectors should be computed.

| ID | Description |
| --- | --- |
| SVDJHV_V | N columns of V are returned in the array V |
| SVDJHV_J | N columns of V are returned in the array V, but they are computed as the product of Jacobi rotations |
| SVDJHV_N | V is not computed |

ENUM_SVDJH_R

An enumeration that defines the range of values to be computed.

| ID | Description |
| --- | --- |
| SVDJHR_N | Do not kill small columns of c*A. |
| SVDJHR_R | RESTRICTED range for sigma(c*A). This option is recommended. |

ENUM_SVDJH_T

An enumeration that specifies whether a matrix should be transposed if it is square.

| ID | Description |
| --- | --- |
| SVDJHT_T | Transpose if entropy test indicates possibly faster convergence of Jacobi process. |
| SVDJHT_N | Do not use transposition. Do not speculate. |

ENUM_SVDJH_P

An enumeration that specifies the possibility of structured perturbations to remove denormalized values.

| ID | Description |
| --- | --- |
| SVDJHP_P | Introduce perturbation. |
| SVDJHP_N | Do not perturb. |

See also

[SingularValueDecompositionDC](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositiondc), [SingularValueDecompositionQR](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionqr)
