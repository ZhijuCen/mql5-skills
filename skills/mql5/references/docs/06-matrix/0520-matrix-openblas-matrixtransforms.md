# Reductions

Functions designed to transform matrices into special forms using orthogonal transformations. These methods are widely used in numerical computations, such as spectral analysis, eigenvalue problems, and singular value decomposition (SVD) of matrices.

These functions enable efficient matrix transformations essential for solving linear algebra problems, including computing Singular Value Decomposition (SVD) and finding eigenvalues of symmetric matrices. The use of LAPACK functions ensures high performance and computational accuracy.

| Function | Action |
| --- | --- |
| ReduceToBidiagonal | Reduces a general real or complex m-by-n matrix A to upper or lower bidiagonal form B by an orthogonal transformation: Q**T * A * P = B. If m >= n, B is upper bidiagonal; if m < n, B is lower bidiagonal. LAPACK function  GEBRD . |
| ReflectBidiagonalToQP | Generates orthogonal matrices Q and P**T (or P**H for complex types) determined by  ReduceToBidiagonal  method when reducing a real or complex matrix A to bidiagonal form: A = Q * B * P**T.  Q and P**T are defined as products of elementary reflectors H(i) or G(i) respectively. LAPACK functions  ORGBR ,  UNGBR . |
| ReduceSymmetricToTridiagonal | Reduces a real symmetric or complex Hermitian matrix A to trdiagonal form B by an orthogonal similarity transformation: Q**T * A * Q = B. LAPACK functions  SYTRD ,  HETRD . |
| ReflectTridiagonalToQ | Generates orthogonal matrix Q  which is defined as the product of n-1 elementary reflectors of order n, as returned by  ReduceSymmetricToTridiagonal |
| ReduceToHessenberg | Reduces a real or complex general n-by-n matrix A to upper Hessenberg form B by an orthogonal similarity transformation: Q**T * A * Q = H. LAPACK function  GEHRD . |
| ReflectHessenbergToQ | Generates orthogonal matrix Q  which is defined as the product of n-1 elementary reflectors of order n, as returned by  ReduceToHessenberg : Q = H(1) H(2) . . . H(n-1). LAPACK function  ORGHR . |
