# General Matrices

Functions for calculating eigenvalues and eigenvectors of a square matrix using classical algorithms. It provides various methods for working with both real and complex matrices, allowing you to solve linear algebra problems with a choice of methods for calculating eigenvectors.

| Function | Action |
| --- | --- |
| EigenSolver | Compute eigenvalues and eigenvectors of a regular square matrix using the classical algorithm (LAPACK function  GEEV ). |
| EigenSolverX | Compute eigenvalues and eigenvectors of a regular square matrix in Expert mode, i.e. with the ability to influence the computation algorithm and the ability to obtain accompanying computation data (LAPACK function  GEEVX ). |
| EigenSolverSchur | Compute eigenvalues, upper triangular matrix in Schur form, and matrix of Schur vectors (LAPACK function  GEES ). See also  Schur decomposition . |
| EigenSolver2 | Compute generalized eigenvalues and eigenvectors for a pair of ordinary square matrices (LAPACK function  GGEV ). |
| EigenSolver2X | Compute generalized eigenvalues and eigenvectors for a pair of regular square matrices in Expert mode, i.e. with the ability to influence the computation algorithm and the ability to obtain accompanying computation data (LAPACK function  GGEVX ). Both matrices must be the same size. |
| EigenSolver2Schur | Compute a pair of ordinary square matrices of generalized eigenvalues,  generalized eigenvectors, generalized Schur forms, as well as left and right Schur vectors (LAPACK function  GGES ). |
| EigenSolver2Blocked | Compute generalized eigenvalues and eigenvectors for a pair of regular square matrices using a block algorithm (LAPACK function  GGEV3 ). Both matrices must be the same size. The method parameters are exactly the same as  EigenSolver2 . |
| EigenSolver2SchurBlocked | Compute a pair of regular square matrices of generalized eigenvalues,  generalized eigenvectors, generalized Schur forms, as well as left and right Schur vectors (LAPACK function  GGES3 ). |
| EigenHessenbergSchurQ | Computes the eigenvalues of a Hessenberg matrix H and the matrices T and Z from the Schur decomposition H = Z T Z**T, where T is an upper quasi-triangular matrix (the Schur form), and Z is the orthogonal matrix of Schur vectors. LAPACK function  HSEQR . See also  Schur decomposition . |
| EigenVectorsTriangularZ | Computes eigenvectors of an real upper quasi-triangular or complex upper triangular matrix computed by  EigenHessenbergSchurQ  or  EigenSolverSchur . A = Q * T * Q**H, where T is an upper quasi-triangular matrix (the Schur form), and Q is the orthogonal matrix of Schur vectors. LAPACK function  TREVC . |
| EigenVectorsTriangularZBlocked | Computes eigenvectors of an real upper quasi-triangular or complex upper triangular matrix computed by  EigenHessenbergSchurQ  or  EigenSolverSchur . A = Q * T * Q**H, where T is an upper quasi-triangular matrix (the Schur form), and Q is the orthogonal matrix of Schur vectors. LAPACK function  TREVC3 . This is the block version (OpenBLAS level 3) of  TREVC . Faster but not so accurate. |
