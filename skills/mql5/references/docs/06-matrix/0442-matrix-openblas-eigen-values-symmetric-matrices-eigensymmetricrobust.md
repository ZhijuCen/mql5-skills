# EigenSymmetricRobust

Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugated) matrix using the Multiple Relatively Robust Representations, MRRR algorithm (LAPACK functions [SYEVR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/syevr.html), [HEEVR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/heevr.html)).

Computing for type matrix<double>

```
bool  matrix::EigenSymmetricRobust(
   ENUM_EIG_VALUES       jobv,               // compute eigenvectors or not
   ENUM_BLAS_RANGE       range,              // subset of eigenvalues to compute
   double                lower,              // lower bound of the subset
   double                upper,              // Upper bound of the subset
   double                abstol,             // absolute error tolerance
   vector&               eigen_values,       // vector of computed eigenvectors
   matrix&               eigen_vectors       // matrix of computed eigenvectors
   );

```

Computing for type matrix<float>

```
bool  matrixf::EigenSymmetricRobust(
   ENUM_EIG_VALUES       jobv,               // compute eigenvectors or not
   ENUM_BLAS_RANGE       range,              // subset of eigenvalues to compute
   float                 lower,              // lower bound of the subset
   float                 upper,              // upper bound of the subset
   float                 abstol,             // absolute error tolerance
   vectorf&              eigen_values,       // vector of computed eigenvectors
   matrixf&              eigen_vectors       // matrix of computed eigenvectors
   );

```

Computing for type matrix<complex>

```
bool  matrixc::EigenSymmetricRobust(
   ENUM_EIG_VALUES       jobv,               // compute eigenvectors or not
   ENUM_BLAS_RANGE       range,              // subset of eigenvalues to compute
   double                lower,              // lower bound of the subset
   double                upper,              // Upper bound of the subset
   double                abstol,             // absolute error tolerance
   vector&               eigen_values,       // vector of computed eigenvectors
   matrixc&              eigen_vectors       // matrix of computed eigenvectors
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::EigenSymmetricRobust(
   ENUM_EIG_VALUES       jobv,               // compute eigenvectors or not
   ENUM_BLAS_RANGE       range,              // subset of eigenvalues to compute
   float                 lower,              // lower bound of the subset
   float                 upper,              // Upper bound of the subset
   float                 abstol,             // absolute error tolerance
   vectorf&              eigen_values,       // vector of computed eigenvectors
   matrixcf&             eigen_vectors       // matrix of computed eigenvectors
   );

```

Parameters

jobv

[in]  [ENUM_EIG_VALUES](/en/docs/matrix/openblas/eigen_values/symmetric_matrices/eigensymmetricdc#enum_eig_values) enumeration value which determines the method for computing eigenvectors.

range

[in]  [ENUM_BLAS_RANGE](/en/docs/matrix/openblas/singular_value_decomposition/singularvaluedecompositionbise) enumeration value that defines a subset of computable eigenvalues and vectors.

lower

[in]  The lower bound of eigenvalues subset; it is specified depending on the value of the 'range' parameter.

upper

[in]  The upper bound of eigenvalues subset; it is specified depending on the value of the 'range' parameter.

abstol

[in]  Absolute error tolerance.

The absolute error tolerance to which each eigenvalue/eigenvector is required.

If jobv = 'V', the eigenvalues and eigenvectors output have residual norms bounded by abstol, and the dot products between different eigenvectors are bounded by abstol.

If abstol < n *eps*|T|, then n *eps*|T| is used instead, where eps is the machine precision, and |T| is the 1-norm of the matrix T. The eigenvalues are computed to an accuracy of eps*|T| irrespective of abstol.

If high relative precision is important, 'abstol' should be set to a safe minimum value X such that 1.0/X does not overflow.

eigen_values

[out] Vector of eigenvalues.

eigen_vectors

[out] Matrix of eigenvectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Computation depends on the values of the jobv and range parameters.

When BLASRANGE_A is set, all eigenvalues are computed, and the lower and upper parameters are ignored.

With the BLASRANGE_V value, only those eigenvalues (and their vectors) are computed, which fall within the range of real values specified by the 'lower' and 'upper' parameters.

With the BLASRANGE_I value, only those eigenvalues (and their vectors) are computed, which fall within the range of integer indices specified by the 'lower' and 'upper' parameters. For example, with lower=0 and upper=2, only the first three eigenvalues are computed.

The input can be a symmetric (Hermitian), [upper triangular](/en/docs/matrix/matrix_manipulations/matrix_triu) or [lower triangular](/en/docs/matrix/matrix_manipulations/matrix_tril) matrix. Triangular matrices are assumed to be symmetric (Hermitian conjugated).

ENUM_EIG_VALUES

An enumeration defining the need to compute eigenvectors.

| ID | Description |
| --- | --- |
| EIGVALUES_V | Eigenvectors and eigenvalues are calculated. |
| EIGVALUES_N | Only eigenvalues are computed, without vectors. |

ENUM_BLAS_RANGE

An enumeration defining how right singular vectors should be computed.

| ID | Description |
| --- | --- |
| BLASRANGE_A | All singular or eigenvalues will be found. |
| BLASRANGE_V | All singular or eigenvalues in the half-open interval (VL,VU] will be found. |
| BLASRANGE_I | The IL-th through IU-th singular or eigenvalues will be found. |
