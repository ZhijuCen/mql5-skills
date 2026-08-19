# EigenSolver2SchurBlocked

Compute a pair of regular square matrices of generalized eigenvalues,  generalized eigenvectors, generalized Schur forms, as well as left and right Schur vectors (LAPACK function [GGES3](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gges3.html)).

Сomputes the generalized eigenvalues, the generalized real/complex Schur form (S,T), optionally, the left and/or right matrices of Schur vectors (VSL and VSR) for a pair of n-by-n real/complex nonsymmetric matrices (A,B). This gives the generalized Schur factorization:

(A,B) = ( vsl*S *vsrH, vsl*T*vsrH )

Optionally, it also orders the eigenvalues so that a selected cluster of eigenvalues appears in the leading diagonal blocks of the upper quasi-triangular matrix S and the upper triangular matrix T. The leading columns of vsl and vsr then form an orthonormal/unitary basis for the corresponding left and right eigenspaces (deflating subspaces).

Computing for type matrix<double>

```
bool  matrix::EigenSolver2SchurBlocked(
   matrix&                B,        // second matrix in the pair
   ENUM_EIG_VECTORS       jobvs,    // method to compute left and right vectors
   vectorc&               alpha,    // vector of computed eigenvalues
   vector&                beta,     // vector of eigenvalue divisors
   matrix&                schur_s,  // matrix S in Schur form
   matrix&                schur_t,  // matrix T in Schur form
   matrix&                vsl,      // matrix of left Schur vectors VSL
   matrix&                vsr       // matrix of right Schur vectors VSR
   );

```

Computing for type matrix<float>

```
bool  matrix::EigenSolver2SchurBlocked(
   matrixf&               B,        // second matrix in the pair
   ENUM_EIG_VECTORS       jobvs,    // method to compute left and right vectors
   vectorcf&              alpha,    // vector of computed eigenvalues
   vectorf&               beta,     // vector of eigenvalue divisors
   matrixf&               schur_s,  // matrix S in Schur form
   matrixf&               schur_t,  // matrix T in Schur form
   matrixf&               vsl,      // matrix of left Schur vectors VSL
   matrixf&               vsr       // matrix of right Schur vectors VSR
   );

```

Computing for type matrix<complex>

```
bool  matrix::EigenSolver2SchurBlocked(
   matrixc&               B,        // second matrix in the pair
   ENUM_EIG_VECTORS       jobvs,    // method to compute left and right vectors
   vectorc&               alpha,    // vector of computed eigenvalues
   vectorc&               beta,     // vector of eigenvalue divisors
   matrixc&               schur_s,  // matrix S in Schur form
   matrixc&               schur_t,  // matrix T in Schur form
   matrixc&               vsl,      // matrix of left Schur vectors VSL
   matrixc&               vsr       // matrix of right Schur vectors VSR
   );

```

Computing for type matrix<complexf>

```
bool  matrix::EigenSolver2SchurBlocked(
   matrixcf&              B,        // second matrix in the pair
   ENUM_EIG_VECTORS       jobvs,    // method to compute left and right vectors
   vectorcf&              alpha,    // vector of computed eigenvalues
   vectorcf&              beta,     // vector of eigenvalue divisors
   matrixcf&              schur_s,  // matrix S in Schur form
   matrixcf&              schur_t,  // matrix T in Schur form
   matrixcf&              vsl,      // matrix of left Schur vectors VSL
   matrixcf&              vsr       // matrix of right Schur vectors VSR
   );

```

Parameters

B

[in]  The second matrix in the pair.

jobvs

[in]  [ENUM_EIG_VECTORS](/en/docs/matrix/openblas/eigen_values/general_matrices/eigensolver#enum_eig_vectors) enumeration value which determines the method for computing left and right eigenvectors.

alpha

[out]  Vector of eigenvalues.

beta

[out]  Vector of eigenvalue divisors.

schur_s

[out]  Matrix S, block upper triangular Schur matrix (Schur form for the input matrix).

schur_t

[out]  Matrix T, block upper triangular Schur matrix (Schur form for the second matrix in the pair).

vsl

[out]  Matrix of left Schur vectors VSL.

vsr

[out]  Matrix of right Schur vectors VSR.

Return Value

The function returns 'true' on success or 'false' if an [error](/en/docs/constants/errorswarnings/errorcodes) occurs.

Note

Computation depends on the jobvs parameter values.

The second matrix in the pair must be the same size as the first (input) one.

Real (non-complex) matrices can have a complex solution. Therefore, the vector of eigenvalues must be complex. In case of a complex solution, the error code is set to [4019 (ERR_MATH_OVERFLOW)](/en/docs/constants/errorswarnings/errorcodes). Otherwise, only the real parts of the complex values of the eigenvalue vector should be used.

EigenSolverSchur

An enumeration defining the need to compute eigenvectors.

| ID | Description |
| --- | --- |
| EIGVECTORS_N | Only eigenvalues are computed, without vectors. |
| EIGVECTORS_L | Only left eigenvectors are computed. |
| EIGVECTORS_R | Only right eigenvectors are computed. |
| EIGVECTORS_LR | Left and right eigenvectors are computed, eigenvalues are always computed. |
