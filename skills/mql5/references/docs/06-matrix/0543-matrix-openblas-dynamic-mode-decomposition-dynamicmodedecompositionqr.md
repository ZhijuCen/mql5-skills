# DynamicModeDecompositionQR

Compute the Dynamic Mode Decomposition (DMD) for a pair of data snapshot matrices, using a QR factorization based compression of the data. LAPACK function GEDMDQ. For the input matrices X and Y such that Y = A*X with an unaccessible matrix A, GEDMDQ computes a certain number of Ritz pairs of A using the standard Rayleigh-Ritz extraction from a subspace of  range(X) that is determined using the leading left singular vectors of X. Optionally, GEDMDQ returns the residuals of the computed Ritz pairs, the information needed for a refinement of the Ritz vectors, or the eigenvectors of the Exact DMD.

The input M-by-N matrix F. The columns of F are the sequence of data snapshots from a single trajectory, taken at equidistant discrete times. It is assumed that the column norms of F are in the range of the normalized floating point numbers. Unlike the [DynamicModeDecomposition](/en/docs/matrix/openblas/dynamic_mode_decomposition/dynamicmodedecomposition) method, where the matrices X(M,N) and Y(M,N) are treated separately, here they are combined into a single state matrix F(M,N+1), such that each current state is associated with the subsequent state. Therefore, M≤N+1.

Computing for type matrix<double>

```
bool  matrix::DynamicModeDecompositionQR(
   ENUM_DMD_SCALE        jobs,                    // determines whether the initial data snapshots are scaled by a diagonal matrix
   ENUM_DMDQ_EIGV        jobz,                    // determines whether the eigenvectors (Koopman modes) will be computed
   ENUM_DMD_RESIDUALS    jobr,                    // determines whether to compute the residuals
   ENUM_DMDQ_Q           jobq,                    // specifies whether to explicitly compute and return the unitary matrix from the QR factorization
   ENUM_DMDQ_R           jobt,                    // specifies whether to return the upper triangular factor from the QR factorization
   ENUM_DMD_REFINE       jobf,                    // specifies whether to store information needed for post-processing
   ENUM_SVD_ALG          whtsvd,                  // allows for a selection of the SVD algorithm from the LAPACK library
   long                  nrnk,                    // determines the mode how to compute the numerical rank
   double                tol,                     // the tolerance for truncating small singular values
   vectorc&              eigen_values,            // vector of eigenvalues (Ritz values)
   matrix&               Q,                       // Q factor from the QR factorization
   matrix&               R,                       // R factor from the QR factorization
   matrix&               left_vectors,            // matrix of left singular vectors
   matrix&               Z                        // matrix of Ritz vectors
   vector&               residuals,               // residuals for the Ritz pairs
   matrix&               B,                       // computed vectors
   matrix&               V,                       // eigenvectors of the matrix Rayleigh quotient
   matrix&               S                        // computed vectors
   );

```

Computing for type matrix<float>

```
bool  matrixf::DynamicModeDecompositionQR(
   ENUM_DMD_SCALE        jobs,                    // determines whether the initial data snapshots are scaled by a diagonal matrix
   ENUM_DMDQ_EIGV        jobz,                    // determines whether the eigenvectors (Koopman modes) will be computed
   ENUM_DMD_RESIDUALS    jobr,                    // determines whether to compute the residuals
   ENUM_DMDQ_Q           jobq,                    // specifies whether to explicitly compute and return the unitary matrix from the QR factorization
   ENUM_DMDQ_R           jobt,                    // specifies whether to return the upper triangular factor from the QR factorization
   ENUM_DMD_REFINE       jobf,                    // specifies whether to store information needed for post-processing
   ENUM_SVD_ALG          whtsvd,                  // allows for a selection of the SVD algorithm from the LAPACK library
   long                  nrnk,                    // determines the mode how to compute the numerical rank
   float                 tol,                     // the tolerance for truncating small singular values
   vectorcf&             eigen_values,            // vector of eigenvalues (Ritz values)
   matrixf&              Q,                       // Q factor from the QR factorization
   matrixf&              R,                       // R factor from the QR factorization
   matrixf&              left_vectors,            // matrix of left singular vectors
   matrixf&              Z                        // matrix of Ritz vectors
   vectorf&              residuals,               // residuals for the Ritz pairs
   matrixf&              B,                       // computed vectors
   matrixf&              V,                       // eigenvectors of the matrix Rayleigh quotient
   matrixf&              S                        // computed vectors
   );

```

Computing for type matrix<complex>

```
bool  matrixc::DynamicModeDecompositionQR(
   ENUM_DMD_SCALE        jobs,                    // determines whether the initial data snapshots are scaled by a diagonal matrix
   ENUM_DMDQ_EIGV        jobz,                    // determines whether the eigenvectors (Koopman modes) will be computed
   ENUM_DMD_RESIDUALS    jobr,                    // determines whether to compute the residuals
   ENUM_DMDQ_Q           jobq,                    // specifies whether to explicitly compute and return the unitary matrix from the QR factorization
   ENUM_DMDQ_R           jobt,                    // specifies whether to return the upper triangular factor from the QR factorization
   ENUM_DMD_REFINE       jobf,                    // specifies whether to store information needed for post-processing
   ENUM_SVD_ALG          whtsvd,                  // allows for a selection of the SVD algorithm from the LAPACK library
   long                  nrnk,                    // determines the mode how to compute the numerical rank
   double                tol,                     // the tolerance for truncating small singular values
   vectorc&              eigen_values,            // vector of eigenvalues (Ritz values)
   matrixc&              Q,                       // Q factor from the QR factorization
   matrixc&              R,                       // R factor from the QR factorization
   matrixc&              left_vectors,            // matrix of left singular vectors
   matrixc&              Z                        // matrix of Ritz vectors
   vector&               residuals,               // residuals for the Ritz pairs
   matrixc&              B,                       // computed vectors
   matrixc&              V,                       // eigenvectors of the matrix Rayleigh quotient
   matrixc&              S                        // computed vectors
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::DynamicModeDecompositionQR(
   ENUM_DMD_SCALE        jobs,                    // determines whether the initial data snapshots are scaled by a diagonal matrix
   ENUM_DMDQ_EIGV        jobz,                    // determines whether the eigenvectors (Koopman modes) will be computed
   ENUM_DMD_RESIDUALS    jobr,                    // determines whether to compute the residuals
   ENUM_DMDQ_Q           jobq,                    // specifies whether to explicitly compute and return the unitary matrix from the QR factorization
   ENUM_DMDQ_R           jobt,                    // specifies whether to return the upper triangular factor from the QR factorization
   ENUM_DMD_REFINE       jobf,                    // specifies whether to store information needed for post-processing
   ENUM_SVD_ALG          whtsvd,                  // allows for a selection of the SVD algorithm from the LAPACK library
   long                  nrnk,                    // determines the mode how to compute the numerical rank
   float                 tol,                     // the tolerance for truncating small singular values
   vectorcf&             eigen_values,            // vector of eigenvalues (Ritz values)
   matrixcf&             Q,                       // Q factor from the QR factorization
   matrixcf&             R,                       // R factor from the QR factorization
   matrixcf&             left_vectors,            // matrix of left singular vectors
   matrixcf&             Z                        // matrix of Ritz vectors
   vectorf&              residuals,               // residuals for the Ritz pairs
   matrixcf&             B,                       // computed vectors
   matrixcf&             V,                       // eigenvectors of the matrix Rayleigh quotient
   matrixcf&             S                        // computed vectors
   );

```

Parameters

jobs

[in]  Value from the [ENUM_DMD_SCALE](/en/docs/matrix/openblas/dynamic_mode_decomposition/dynamicmodedecomposition#enum_dmd_scale) enumeration which determines whether the initial data snapshots are scaled by a diagonal matrix. The data snapshots are the columns of F. The leading N-1 columns of F are denoted X and the trailing N-1 columns are denoted Y.

jobz

[in]   Value from the [ENUM_DMDQ_EIGV](/en/docs/matrix/openblas/dynamic_mode_decomposition/dynamicmodedecomposition#enum_dmd_eigv) enumeration which determines whether the eigenvectors (Koopman modes) will be computed.

jobr

[in]   Value from the [ENUM_DMD_RESIDUALS](/en/docs/matrix/openblas/dynamic_mode_decomposition/dynamicmodedecomposition#enum_dmd_residuals) enumeration which determines whether to compute the residuals.

jobq

[in]   Value from the [ENUM_DMDQ_Q](/en/docs/matrix/openblas/dynamic_mode_decomposition/dynamicmodedecompositionqr#enum_dmdq_q) enumeration which specifies whether to explicitly compute and return the unitary matrix from the QR factorization of the data snapshot matrix.

jobt

[in]   Value from the [ENUM_DMDQ_R](/en/docs/matrix/openblas/dynamic_mode_decomposition/dynamicmodedecompositionqr#enum_dmdq_r) enumeration which specifies whether to return the upper triangular factor from the QR factorization of the data snapshot matrix.

jobf

[in]   Value from the [ENUM_DMD_REFINE](/en/docs/matrix/openblas/dynamic_mode_decomposition/dynamicmodedecomposition#enum_dmd_refine) enumeration which specifies whether to store information needed for post-processing (e.g. computing refined Ritz vectors).

whtsvd

[in]   Value from the [ENUM_SVD_ALG](/en/docs/matrix/openblas/dynamic_mode_decomposition/dynamicmodedecomposition#enum_svd_alg) enumeration which allows for a selection of the SVD algorithm from the LAPACK library.

nrnk

[in]   Value determines the mode how to compute the numerical rank, i.e. how to truncate small singular values of the input matrix X. If

NRNK = -1 :: i-th singular value sigma(i) is truncated if sigma(i) <= TOL*sigma(1). This option is recommended.

NRNK = -2 :: i-th singular value sigma(i) is truncated if sigma(i) <= TOL*sigma(i-1). This option is included for R&D purposes. It requires highly accurate SVD, which may not be feasible.

The numerical rank can be enforced by using positive value of NRNK as follows: 0 < NRNK <= N-1 :: at most NRNK largest singular values will be used. If the number of the computed nonzero singular values is less than NRNK, then only those nonzero values will be used and the actually used dimension is less than NRNK.

tol

[in]   The tolerance for truncating small singular values. 0 <= TOL < 1

eigen_values

[out] Vector of eigenvalues of size K. The leading K (K<N) entries of EIGS contain the computed eigenvalues (Ritz values).

Q

[out]  Orthogonal matrix/factor of the QR factorization of the initial data snapshots matrix F.

R

[out]  N-by-N upper triangular factor from the QR factorization of the data snapshot matrix F.

left_vectors

[out] Matrix of left singular vectors. The leading K columns of X contain the leading K left singular vectors of the hold representations of the leading N-1 snapshots in the orthonormal basis computed in the QR factorization of F. To lift them to the space of the left singular vectors U(:,1:K) of the input data, pre-multiply with the Q factor from the initial QR factorization.

Z

[out] M-by-K matrix

If JOBZ =='V' then Z contains the Ritz vectors. Z(:,i) is an eigenvector of the i-th Ritz value; ||Z(:,i)||_2=1.

If JOBZ == 'F', then the Z(:,i)'s are given implicitly as Z*V, where Z contains orthonormal matrix (the product of Q from the initial QR factorization and the SVD/POD_basis returned by GEDMD in X) and the second factor (the eigenvectors of the Rayleigh quotient) is in the matrix V, as returned by GEDMD. That is,  X(:,1:K)*V(:,i) is an eigenvector corresponding to EIGS(i). The columns of V(1:K,1:K) are the computed eigenvectors of the K-by-K Rayleigh quotient.

residuals

[out]  Residuals for the K computed Ritz pairs.

B

[out]  N-by-K matrix (K<N).

If JOBF =='R', B(1:N,1:K) contains A*U(:,1:K), and can be used for computing the refined vectors.

If JOBF == 'E', B(1:N,1;K) contains A*U(:,1:K)*W(1:K,1:K), which are the vectors from the Exact DMD, up to scaling by the inverse eigenvalues.

In both cases, the content of B can be lifted to the original dimension of the input data by pre-multiplying with the Q factor from the initial QR factorization. Here A denotes a compression of the underlying operator.

If JOBF =='N', then B is not referenced.

V

[out]  K-by-K matrix (K<N). Contains the the K eigenvectors of the Rayleigh quotient. The Ritz vectors (returned in Z) are the product of Q from the initial QR factorization.

S

[out]  K-by-K matrix (K<N). The array S(1:K,1:K) is used for the matrix Rayleigh quotient. This content is overwritten during the eigenvalue decomposition by [GEEV](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/geev.html).

Return Value

The function returns 'true' on success or 'false' if an [error](/en/docs/constants/errorswarnings/errorcodes) occurs.

Note

The number of matrices rows (M) must not be less than the number of columns (N).

ENUM_DMD_SCALE

An enumeration that determines whether the initial data snapshots are scaled by a diagonal matrix.

| ID | Description |
| --- | --- |
| DMDSCALE_S | 'S': The data snapshots matrices X and Y are multiplied with a diagonal matrix D so that X*D has unit nonzero columns |
| DMDSCALE_C | 'C': The snapshots are scaled as with the 'S' option.If it is found that an i-th column of X is zero vector and the corresponding i-th column of Y is non-zero, then the i-th column of Y is set to zero |
| DMDSCALE_Y | 'Y': The data snapshots matrices X and Y are multiplied with a diagonal matrix D so that Y*D has unit nonzero columns |
| DMDSCALE_N | 'N': No data scaling |

ENUM_DMDQ_EIGV

An enumeration which determines whether the eigenvectors (Koopman modes) will be computed.

| ID | Description |
| --- | --- |
| DMDQEIGV_V | 'V': The eigenvectors (Koopman modes) will be computed |
| DMDQEIGV_F | 'F': The eigenvectors (Koopman modes) will be returned in factored form as the product Z*V |
| DMDQEIGV_Q | 'Q': The eigenvectors (Koopman modes) will be returned in factored form as the product Q*Z |
| DMDQEIGV_N | 'N': The eigenvectors are not computed |

ENUM_DMD_RESIDUALS

An enumeration which determines whether to compute the residuals.

| ID | Description |
| --- | --- |
| DMDRESIDUALS_R | 'R': The residuals for the computed eigenpairs will be computed |
| DMDRESIDUALS_N | 'N': The residuals are not computed |

ENUM_DMDQ_Q

An enumeration which specifies whether to explicitly compute and return the unitary matrix from the QR factorization.

| ID | Description |
| --- | --- |
| DMDQQ_Q | 'Q': The matrix Q of the QR factorization of the data snapshot matrix is computed |
| DMDQQ_N | 'N': The matrix Q is not explicitly computed |

ENUM_DMDQ_R

An enumeration whichspecifies whether to return the upper triangular factor from the QR factorization.

| ID | Description |
| --- | --- |
| DMDQR_R | 'R': The matrix R of the QR factorization of the data snapshot matrix is computed |
| DMDQR_N | 'N': The matrix R is not explicitly computed |

ENUM_DMD_REFINE

An enumeration which specifies whether to store information needed for post-processing.

| ID | Description |
| --- | --- |
| DMDREFINE_R | 'R': The matrix needed for the refinement of the Ritz vectors is computed and stored in the array B |
| DMDREFINE_E | 'E': The unscaled eigenvectors of the Exact DMD are computed and returned in the array B |
| DMDREFINE_N | 'N': No eigenvector refinement data is computed |

ENUM_SVD_ALG

An enumeration selecting the SVD algorythm.

| ID | Description |
| --- | --- |
| SVDALG_1 | 1:  GESVD  (the QR SVD algorithm) |
| SVDALG_2 | 2:  GESDD  (the Divide and Conquer algorithm) |
| SVDALG_3 | 3:  GESVDQ  (the preconditioned QR SVD; this and 4 are the most accurate options) |
| SVDALG_4 | 4:  GEJSV  (the preconditioned Jacobi SVD; this and 3 are the most accurate options) |
