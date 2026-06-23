# SylvesterEquationSchur

Solves Sylvester equation for real quasi-triangular or complex triangular matrices:

A*X + X*B = C

where  A and B are both upper triangular. A is m-by-m and B is n-by-n; the right hand side C and the solution X are m-by-n.

A and B must be in Schur canonical form (as returned by [EigenHessenbergSchurQ](/en/docs/matrix/openblas/eigen_values/general_matrices/eigenhessenbergschurq) or [EigenSolverSchur](/en/docs/matrix/openblas/eigen_values/general_matrices/eigensolverschur)), that is, in case of real quasi-triangular, block upper triangular with 1-by-1 and 2-by-2 diagonal blocks; each 2-by-2 diagonal block has its diagonal elements equal and its off-diagonal elements of opposite sign.

LAPACK function [TRSYL](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/trsyl.html).

Computing for type matrix<double>

```
bool  matrix::SylvesterEquationSchur(
   matrix&              B,            // matrix B in Schur form
   matrix&              QA,           // orthogonal matrix of Schur vectors of the input matrix A
   matrix&              QB,           // orthogonal matrix of Schur vectors of the matrix B
   matrix&              C,            // right hand side matrix C
   matrix&              X             // solution matrix X
   );

```

Computing for type matrix<float>

```
bool  matrixf::SylvesterEquationSchur(
   matrixf&             B,            // matrix B in Schur form
   matrixf&             QA,           // orthogonal matrix of Schur vectors of the input matrix A
   matrixf&             QB,           // orthogonal matrix of Schur vectors of the matrix B
   matrixf&             C,            // right hand side matrix C
   matrixf&             X             // solution matrix X
   );

```

Computing for type matrix<complex>

```
bool  matrix::SylvesterEquationSchur(
   matrixc&             B,            // matrix B in Schur form
   matrixc&             QA,           // orthogonal matrix of Schur vectors of the input matrix A
   matrixc&             QB,           // orthogonal matrix of Schur vectors of the matrix B
   matrixc&             C,            // right hand side matrix C
   matrixc&             X             // solution matrix X
   );

```

Computing for type matrix<complexf>

```
bool  matrix::SylvesterEquationSchur(
   matrixcf&            B,            // matrix B in Schur form
   matrixcf&            QA,           // orthogonal matrix of Schur vectors of the input matrix A
   matrixcf&            QB,           // orthogonal matrix of Schur vectors of the matrix B
   matrixcf&            C,            // right hand side matrix C
   matrixcf&            X             // solution matrix X
   );

```

Parameters

B

[in]  Real quasi-triangular or complex triangular matrix B in Schur form (output parameter schur_matrix in [EigenSolverSchur](/en/docs/matrix/openblas/eigen_values/general_matrices/eigensolverschur) or schur_t in [EigenHessenbergSchurQ](/en/docs/matrix/openblas/eigen_values/general_matrices/eigenhessenbergschurq))

QA

[in]  Real orthogonal or complex unitary matrix of Schur vectors of the original matrix A (output parameter schur_vectors in [EigenSolverSchur](/en/docs/matrix/openblas/eigen_values/general_matrices/eigensolverschur) or schur_z in [EigenHessenbergSchurQ](/en/docs/matrix/openblas/eigen_values/general_matrices/eigenhessenbergschurq))

QB

[in]  Real orthogonal or complex unitary matrix of Schur vectors of the original matrix B (output parameter schur_vectors in [EigenSolverSchur](/en/docs/matrix/openblas/eigen_values/general_matrices/eigensolverschur) or schur_z in [EigenHessenbergSchurQ](/en/docs/matrix/openblas/eigen_values/general_matrices/eigenhessenbergschurq))

C

[in]  Matrix C whose columns are the right-hand sides for the systems of equations.

X

[out]  Matrix X with solution of Sylvester equation.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Output matrix X has the same sizes as input matrix C.

The [TRSYL](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/trsyl.html) function handles only upper triangular matrices A and B. To solve a Sylvester equation for arbitrary square matrices, compute Schur decompositions first. For example, given two general matrices A and B, obtain two Schur decomposition pairs:

A.EigenSolverSchur(EIGSCHUR_V,EV,SA,QA);

B.EigenSolverSchur(EIGSCHUR_V,EV,SB,QB);

and solve the Sylvester equation:

SA.SylvesterEquationSchur(SB,QA,QB,C,X);
