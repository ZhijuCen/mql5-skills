# OpenBLAS Methods

OpenBLAS is a high-performance open-source linear algebra library that implements BLAS (Basic Linear Algebra Subprograms) and some LAPACK functions. OpenBLAS is designed to improve computational performance, particularly in matrix and vector operations, which are often used in scientific and engineering tasks such as machine learning, numerical methods, and simulations.

Key features of OpenBLAS:

- Multithreading support: OpenBLAS can efficiently use multiple processor cores for parallel computations, significantly accelerating operations on multiprocessor systems.
- Optimization for processor architectures: OpenBLAS includes optimized builds for various processors such as Intel, AMD, ARM and others. The library automatically detects processor characteristics and selects the most suitable function implementations.
- Extensive BLAS operation support: OpenBLAS implements core BLAS functions, including vector operations (e.g., vector addition and dot product), matrix operations (multiplication), and vector-matrix operations.
- LAPACK compatibility: The library supports LAPACK (Linear Algebra PACKage) functions for more complex linear algebra operations, such as solving systems of linear equations, calculating matrix eigenvalues, and others.

- High performance: Compared to other BLAS libraries, OpenBLAS often shows better results due to hand-optimization for specific processor architectures.

### Applications

OpenBLAS is widely used in applications involving numerical computations:

- Training neural networks and other machine learning tasks.
- Scientific computing (e.g. modeling of physical processes).
- Processing and analyzing large amounts of data.

The library is integrated into many popular scientific software packages such as NumPy, SciPy, and TensorFlow, which rely on high-performance linear algebra operations.

OpenBLAS is an excellent choice for those seeking an open-source solution for high-performance computing, particularly when working with large matrices and vectors.

| Function | Action |
| --- | --- |
| SingularValueDecompositionDC | Singular Value Decomposition, "divide-and-conquer" algorithm. This algorithm is considered the fastest among other SVD algorithms (LAPACK function GESDD). |
| SingularValueDecompositionQR | Singular Value Decomposition, QR algorithm. This algorithm is considered a classical SVD algorithm (LAPACK function GESVD). |
| SingularValueDecompositionQRPivot | Singular Value Decomposition, QR with pivoting algorithm (LAPACK function GESVDQ). |
| SingularValueDecompositionBisect | Singular Value Decomposition, bisection algorithm (LAPACK function GESVDX). |
| SingularValueDecompositionJacobiHigh | Singular Value Decomposition, Jacobi high level algorithm (LAPACK function GEJSV). |
| SingularValueDecompositionJacobiLow | Singular Value Decomposition, Jacobi low level algorithm (LAPACK function GESVJ). The method computes small singular values and their singular vectors with much greater accuracy than other SVD routines in certain cases. |
| SingularValueDecompositionBidiagDC | Singular Value Decomposition, divide-and-conquer algorithm for bidiagonal matrices (LAPACK function BDSVDX). |
| SingularValueDecompositionBidiagBisect | Singular Value Decomposition, bisection algorithm for bidiagonal matrices (LAPACK function BDSVDX). |
| EigenSolver | Compute eigenvalues and eigenvectors of a regular square matrix using the classical algorithm (LAPACK function GEEV). |
| EigenSolver2 | Compute generalized eigenvalues and eigenvectors for a pair of ordinary square matrices (LAPACK function GGEV). |
| EigenSolverX | Compute eigenvalues and eigenvectors of a regular square matrix in Expert mode, i.e. with the ability to influence the computation algorithm and the ability to obtain accompanying computation data (LAPACK function GEEVX). |
| EigenSolverSchur | Compute eigenvalues, upper triangular matrix in Schur form, and matrix of Schur vectors (LAPACK function GEES). See also  Schur decomposition . |
| EigenSymmetricDC | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugate) matrix using the divide-and-conquer algorithm (LAPACK functions SYEVD, HEEVD). |
| EigenSymmetricQR | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugate) matrix using the QR algorithm (LAPACK functions SYEV, HEEV). |
| EigenSymmetricRobust | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugate) matrix using the Multiple Relatively Robust Representations, MRRR algorithm (LAPACK functions SYEVR, HEEVR). |
| EigenSymmetricBisect | Compute eigenvalues and eigenvectors of a symmetric or Hermitian (complex conjugate) matrix using the bisection algorithm (LAPACK functions SYEVX, HEEVX). |
| SingularSpectrumAnalysisSpectrum | A method function for calculating the relative contributions of spectral components based on their eigenvalues. |
| SingularSpectrumAnalysisForecast | A method function for calculating reconstructed and predicted data using spectral components of the input time series. |
| SingularSpectrumAnalysisReconstructComponents | A method function for calculating reconstructed components of the input time series and their contributions. |
| SingularSpectrumAnalysisReconstructSeries | A method function for calculating the reconstructed time series using the first component_count components. |
