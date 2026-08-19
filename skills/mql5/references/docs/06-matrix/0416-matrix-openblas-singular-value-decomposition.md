# Singular value decomposition

This section features functions for decomposing a matrix into three components: orthogonal matrices and a diagonal matrix of singular values. SVD is applied to solve various linear algebra problems such as data dimensionality reduction, image compression, solving systems of equations, and data analysis and optimization. The main functions allow you to compute singular values and vectors, reconstruct matrices, and approximate matrices with reduced rank accuracy.

| Function | Action |
| --- | --- |
| SingularValueDecompositionDC | Singular Value Decomposition, "divide-and-conquer" algorithm. This algorithm is considered the fastest among other SVD algorithms (LAPACK function  GESDD ). |
| SingularValueDecompositionQR | Singular Value Decomposition, QR algorithm. This algorithm is considered a classical SVD algorithm (LAPACK function  GESVD ). |
| SingularValueDecompositionQRPivot | Singular Value Decomposition, QR with pivoting algorithm (LAPACK function  GESVDQ ). |
| SingularValueDecompositionBisection | Singular Value Decomposition, bisection algorithm (LAPACK function  GESVDX ). |
| SingularValueDecompositionJacobiHigh | Singular Value Decomposition, Jacobi high level algorithm (LAPACK function  GEJSV ). |
| SingularValueDecompositionJacobiLow | Singular Value Decomposition, Jacobi low level algorithm (LAPACK function  GESVJ ). The method computes small singular values and their singular vectors with much greater accuracy than other SVD routines in certain cases. |
| SingularValueDecompositionBidiagDC | Singular Value Decomposition, divide-and-conquer algorithm for bidiagonal matrices (LAPACK function  BDSDC ). |
| SingularValueDecompositionBidiagBisect | Singular Value Decomposition, bisection algorithm for bidiagonal matrices (LAPACK function  BDSVDX ). |
| SingularValueDecompositionBidiagQR | Computes the singular value decomposition of a general matrix that has been reduced to bidiagonal form by the method  ReduceToBidiagonal . LAPACK function  BDSQR . |
