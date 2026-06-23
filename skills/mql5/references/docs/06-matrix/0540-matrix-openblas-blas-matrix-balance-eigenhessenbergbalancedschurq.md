# EigenHessenbergBalancedSchurQ

Computes the eigenvalues of a Hessenberg matrix H and the matrices T and Z from the Schur decomposition H = Z T Z**T, where T is an upper quasi-triangular matrix (the Schur form), and Z is the orthogonal matrix of Schur vectors. Optionally Z may be postmultiplied into an input orthogonal matrix Q so that this routine can give the Schur factorization of a matrix A which has been reduced to the Hessenberg form H by the orthogonal matrix Q:

A = Q*H*Q**T = (QZ)*T*(QZ)**T.

LAPACK function [HSEQR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/hseqr.html).

Computing for type matrix<double>

```
bool  matrix::EigenHessenbergBalancedSchurQ(
   long                  ilo,                     // subscript of balanced matrix
   long                  ihi,                     // superscript of balanced matrix
   matrix&               Q,                       // orthogonal matrix Q
   vectorc&              eigen_values,            // vector of computed eigenvalues
   matrix&               schur_t,                 // matrix T in Schur form
   matrix&               schur_z                  // matrix Z of Schur vectors
   );

```

Computing for type matrix<float>

```
bool  matrixf::EigenHessenbergBalancedSchurQ(
   long                  ilo,                     // subscript of balanced matrix
   long                  ihi,                     // superscript of balanced matrix
   matrixf&              Q,                       // orthogonal matrix Q
   vectorcf&             eigen_values,            // vector of computed eigenvalues
   matrixf&              schur_t,                 // matrix T in Schur form
   matrixf&              schur_z                  // matrix Z of Schur vectors
   );

```

Computing for type matrix<complex>

```
bool  matrixc::EigenHessenbergBalancedSchurQ(
   long                  ilo,                     // subscript of balanced matrix
   long                  ihi,                     // superscript of balanced matrix
   matrixc&              Q,                       // orthogonal matrix Q
   vectorc&              eigen_values,            // vector of computed eigenvalues
   matrixc&              schur_t,                 // matrix T in Schur form
   matrixc&              schur_z                  // matrix Z of Schur vectors
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::EigenHessenbergBalancedSchurQ(
   long                  ilo,                     // subscript of balanced matrix
   long                  ihi,                     // superscript of balanced matrix
   matrixcf&             Q,                       // orthogonal matrix Q
   vectorcf&             eigen_values,            // vector of computed eigenvalues
   matrixcf&             schur_t,                 // matrix T in Schur form
   matrixcf&             schur_z                  // matrix Z of Schur vectors
   );

```

Parameters

ilo

[in]  Subscript of the balanced matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

ihi

[in]  Superscript of the balanced matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

Q

[in]  Orthogonal matrix Q produced by method [ReflectHessenbergBalancedToQ](/en/docs/matrix/openblas/blas_matrix_balance/reflecthessenbergbalancedtoq). Matrix Q can be of zero size, in this case Hessenberg matrix (not original matrix A) will be decomposed. If matrix Q is used, then calculated the original matrix A reduced to Hessenberg form (see [ReduceToHessenbergBalanced](/en/docs/matrix/openblas/blas_matrix_balance/reducetohessenbergbalanced)).

eigen_values

[out] Vector of eigenvalues.

schur_t

[out]  Upper triangular Schur matrix (Schur form for the input matrix).

schur_z

[out]  Matrix of Schur vectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

It is assumed that A is already upper triangular in rows and columns 1:ilo-1 and ihi+1:N. ilo and ihi are normally set by a previous call to [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance), and then passed to [ReduceToHessenbergBalanced](/en/docs/matrix/openblas/blas_matrix_balance/reducetohessenbergbalanced) when the matrix output by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance) is reduced to Hessenberg form. Otherwise they should be set to 1 and N respectively.

Real (non-complex) matrices can have a complex solution. Therefore, the input vector of eigenvalues must be complex. In case of a complex solution, the error code is set to [4019 (ERR_MATH_OVERFLOW)](/en/docs/constants/errorswarnings/errorcodes). Otherwise, only the real parts of the complex values of the eigenvalue vector should be used.
