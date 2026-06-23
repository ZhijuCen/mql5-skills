# Eigen Values

The section features functions for computing eigenvalues and eigenvectors. It describes methods for solving standard linear algebra problems using the LAPACK library algorithms. These functions are efficient for matrix analysis, diagonalization, system stabilization, and other tasks.

- EigenSolver: The function is designed to compute the eigenvalues and eigenvectors of an arbitrary square matrix using the classical algorithm represented by the GEEV LAPACK function. This method is applied to a wide range of matrices, allowing the decomposition of matrices into their eigenvalues and eigenvectors.
- EigenSymmetricDC: The function for computing eigenvalues and eigenvectors of symmetric or Hermitian matrices using the divide-and-conquer algorithm. The LAPACK functions SYEVD and HEEVD enable the efficient handling of symmetric or Hermitian matrices, providing faster and more accurate processing of such matrices.

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
| EigenSymmetricDC | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugate) matrix using the divide-and-conquer algorithm (LAPACK functions  SYEVD ,  HEEVD ). |
| EigenSymmetricQR | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugate) matrix using the QR algorithm (LAPACK functions  SYEV ,  HEEV ). |
| EigenSymmetricRobust | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugate) matrix using the Multiple Relatively Robust Representations, MRRR algorithm (LAPACK functions  SYEVR ,  HEEVR ). |
| EigenSymmetricBisect | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugate) matrix using the bisection algorithm (LAPACK functions  SYEVX ,  HEEVX ). |
| EigenSymmetricDC2s | Compute all eigenvalues and, optionally, eigenvectors of a real symmetric or Hermitian (complex conjugated) matrix using the 2stage technique for the reduction to tridiagonal. If eigenvectors are desired, it uses a divide and conquer algorithm (LAPACK functions SYEVD_2STAGE, HEEVD_2STAGE). |
| EigenSymmetricQR2s | Compute all eigenvalues and, optionally, eigenvectors of a real symmetric or Hermitian (complex conjugated) matrix using the 2stage technique for the reduction to tridiagonal (LAPACK functions  SYEV_2STAGE , HEEV_2STAGE). |
| EigenSymmetricRobust2s | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugated) matrix using the 2stage technique for the reduction to tridiagonal then using the Multiple Relatively Robust Representations, MRRR algorithm (LAPACK functions  SYEVR_2STAGE , HEEVR_2STAGE). |
| EigenSymmetricBisect2s | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugated) matrix using the 2stage technique for the reduction to tridiagonal then using the bisection algorithm (LAPACK functions  SYEVX_2STAGE , HEEVX_2STAGE). |
| EigenSymmetric2DC | Compute all the eigenvalues, and optionally, the eigenvectors of a generalized symmetric-definite eigenproblem, of the form  A*x=(lambda)*B*x,  A*Bx=(lambda)*x,  or B*A*x=(lambda)*x.  LAPACK functions  SYGVD ,  HEGVD . |
| EigenSymmetric2QR | Compute all the eigenvalues, and optionally, the eigenvectors of a generalized symmetric-definite eigenproblem, of the form A*x=(lambda)*B*x,  A*Bx=(lambda)*x,  or B*A*x=(lambda)*x.  LAPACK functions  SYGV ,  HEGV . |
| EigenSymmetric2Bisect | Compute all the eigenvalues, and optionally, the eigenvectors of a generalized symmetric-definite eigenproblem, of the form A*x=(lambda)*B*x,  A*Bx=(lambda)*x,  or B*A*x=(lambda)*x.  LAPACK functions  SYGVX ,  HEGVX . |
| EigenTridiagonalDC | Compute eigenvalues and eigenvectors of a symmetric tridiagonal matrix using the divide-and-conquer algorithm (LAPACK function  STEVD ). |
| EigenTridiagonalQR | Compute eigenvalues and eigenvectors of a symmetric tridiagonal matrix using the QR algorithm (LAPACK function  STEV ). |
| EigenTridiagonalRobust | Compute eigenvalues and eigenvectors of a symmetric tridiagonal matrix using the Multiple Relatively Robust Representations, MRRR algorithm (LAPACK function  STEVR ). |
| EigenTridiagonalBisect | Compute eigenvalues and eigenvectors of a symmetric tridiagonal matrix using the bisection algorithm (LAPACK function  STEVX ). |
| EigenTridiagonalQL | Compute all eigenvalues of a symmetric tridiagonal matrix using the Pal-Walker-Kahan variant of the QL or QR algorithm (LAPACK function  STERF ). |
| EigenTridiagonalDCQ | Compute eigenvalues and eigenvectors of a symmetric tridiagonal matrix using the divide-and-conquer algorithm (LAPACK function  STEDC ). |
| EigenTridiagonalQRQ | Compute eigenvalues and eigenvectors of a symmetric tridiagonal matrix using the QR algorithm (LAPACK function  STEQR ). |
| EigenTridiagonalPosDefQ | Compute eigenvalues and eigenvectors of a symmetric positive definite (положительно определённая) tridiagonal matrix using the QR algorithm (LAPACK function  PTEQR ). |
