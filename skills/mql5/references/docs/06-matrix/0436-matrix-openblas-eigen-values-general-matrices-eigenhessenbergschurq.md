# EigenHessenbergSchurQ

Computes the eigenvalues of a Hessenberg matrix H and the matrices T and Z from the Schur decomposition H = Z T Z**T, where T is an upper quasi-triangular matrix (the Schur form), and Z is the orthogonal matrix of Schur vectors. Optionally Z may be postmultiplied into an input orthogonal matrix Q so that this routine can give the Schur factorization of a matrix A which has been reduced to the Hessenberg form H by the orthogonal matrix Q:

A = Q*H*Q**T = (QZ)*T*(QZ)**T.

LAPACK function [HSEQR](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/hseqr.html). See also [Schur decomposition](https://en.wikipedia.org/wiki/Schur_decomposition).

Computing for type matrix<double>

```
bool  matrix::EigenHessenbergSchurQ(
   matrix&               Q,                       // orthogonal matrix Q
   vectorc&              eigen_values,            // vector of computed eigenvalues
   matrix&               schur_t,                 // matrix T in Schur form
   matrix&               schur_z                  // matrix Z of Schur vectors
   );

```

Computing for type matrix<float>

```
bool  matrixf::EigenHessenbergSchurQ(
   matrixf&              Q,                       // orthogonal matrix Q
   vectorcf&             eigen_values,            // vector of computed eigenvalues
   matrixf&              schur_t,                 // matrix T in Schur form
   matrixf&              schur_z                  // matrix Z of Schur vectors
   );

```

Computing for type matrix<complex>

```
bool  matrixc::EigenHessenbergSchurQ(
   matrixc&              Q,                       // orthogonal matrix Q
   vectorc&              eigen_values,            // vector of computed eigenvalues
   matrixc&              schur_t,                 // matrix T in Schur form
   matrixc&              schur_z                  // matrix Z of Schur vectors
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::EigenHessenbergSchurQ(
   matrixcf&             Q,                       // orthogonal matrix Q
   vectorcf&             eigen_values,            // vector of computed eigenvalues
   matrixcf&             schur_t,                 // matrix T in Schur form
   matrixcf&             schur_z                  // matrix Z of Schur vectors
   );

```

Parameters

Q

[in]  Orthogonal matrix Q produced by method [ReflectHessenbergToQ](/en/docs/matrix/openblas/matrixtransforms/reflecthessenbergtoq). Matrix Q can be of zero size, in this case Hessenberg matrix (not original matrix A) will be decomposed. If matrix Q is used, then calculated the original matrix A reduced to Hessenberg form (see [ReduceToHessenberg](/en/docs/matrix/openblas/matrixtransforms/reducetohessenberg)).

eigen_values

[out] Vector of eigenvalues.

schur_t

[out]  Upper triangular Schur matrix (Schur form for the input matrix).

schur_z

[out]  Matrix of Schur vectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Real (non-complex) matrices can have a complex solution. Therefore, the input vector of eigenvalues must be complex. In case of a complex solution, the error code is set to [4019 (ERR_MATH_OVERFLOW)](/en/docs/constants/errorswarnings/errorcodes). Otherwise, only the real parts of the complex values of the eigenvalue vector should be used.
