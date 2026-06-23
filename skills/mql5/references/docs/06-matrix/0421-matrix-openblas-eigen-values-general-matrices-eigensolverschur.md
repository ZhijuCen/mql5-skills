# EigenSolverSchur

Compute eigenvalues, upper triangular matrix in Schur form, and matrix of Schur vectors (LAPACK function [GEES](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gees.html)). See also [Schur decomposition](https://en.wikipedia.org/wiki/Schur_decomposition).

Computing for type matrix<double>

```
bool  matrix::EigenSolverSchur(
   ENUM_EIG_SCHUR        jobvs,                   // method to compute Schur vectors
   vectorc&              eigen_values,            // vector of computed eigenvalues
   matrix&               schur_matrix,            // matrix in Schur form
   matrix&               schur_vectors            // matrix of Schur vectors
   );

```

Computing for type matrix<float>

```
bool  matrixf::EigenSolverSchur(
   ENUM_EIG_SCHUR        jobvs,                   // method to compute Schur vectors
   vectorcf&             eigen_values,            // vector of computed eigenvalues
   matrixf&              schur_matrix,            // matrix in Schur form
   matrixf&              schur_vectors            // matrix of Schur vectors
   );

```

Computing for type matrix<complex>

```
bool  matrixc::EigenSolverSchur(
   ENUM_EIG_SCHUR        jobvs,                   // method to compute Schur vectors
   vectorc&              eigen_values,            // vector of computed eigenvalues
   matrixc&              schur_matrix,            // matrix in Schur form
   matrixc&              schur_vectors            // matrix of Schur vectors
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::EigenSolverSchur(
   ENUM_EIG_SCHUR        jobvs,                   // method to compute Schur vectors
   vectorcf&             eigen_values,            // vector of computed eigenvalues
   matrixcf&             schur_matrix,            // matrix in Schur form
   matrixcf&             schur_vectors            // matrix of Schur vectors
   );

```

Parameters

jobvs

[in]  Value from the [ENUM_EIG_SCHUR](/en/docs/matrix/openblas/eigen_values/general_matrices/eigensolverschur#eigensolverschur) enumeration, which defines the method for computing Schur vectors.

eigen_values

[out] Vector of eigenvalues.

schur_matrix

[out]  Upper triangular Schur matrix (Schur form for the input matrix).

schur_vectors

[out]  Matrix of Schur vectors; it is not computed if the jobvs parameter is set to N.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Computation depends on the jobvs parameter values.

Real (non-complex) matrices can have a complex solution. Therefore, the input vector of eigenvalues must be complex. In case of a complex solution, the error code is set to [4019 (ERR_MATH_OVERFLOW)](/en/docs/constants/errorswarnings/errorcodes). Otherwise, only the real parts of the complex values of the eigenvalue vector should be used.

ENUM_EIG_SCHUR

An enumeration defining the need to compute eigenvectors.

| ID | Description |
| --- | --- |
| EIGSCHUR_N | Schur vectors are not computed |
| EIGSCHUR_V | Schur vectors are computed |
