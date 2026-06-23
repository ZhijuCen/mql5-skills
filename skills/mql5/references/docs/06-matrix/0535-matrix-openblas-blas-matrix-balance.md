# Matrix Balance

This section presents functions that improve the numerical stability and accuracy of eigenvalue computations by transforming general matrices into balanced forms. Balancing a matrix involves permuting and scaling its rows and columns to reduce its norm and isolate eigenvalues, which can significantly enhance the performance of subsequent algorithms.

These functions are particularly important in preparing matrices for efficient and accurate eigenvalue and Schur decomposition computations. The use of LAPACK functions ensures robust and high-performance linear algebra operations.

| Function | Action |
| --- | --- |
| MatrixBalance | Balances a general real or complex square matrix A. This involves, first, permuting A by a similarity transformation to isolate eigenvalues in the first 1 to ILO-1 and last IHI+1 to N elements on the diagonal; and second, applying a diagonal similarity transformation to rows and columns ILO to IHI to make the rows and columns as close in norm as possible.  Both steps are optional. Balancing may reduce the 1-norm of the matrix, and improve the accuracy of the computed eigenvalues and/or eigenvectors. LAPACK function  GEBAL . |
| EigenVectorsBackward | Forms the right or left eigenvectors of a real or complex general matrix by backward transformation on the computed eigenvectors of the balanced matrix output by  MatrixBalance . LAPACK function  GEBAK . |
| ReduceToHessenbergBalanced | Reduces a real or complex general n-by-n balanced matrix A to upper Hessenberg form B by an orthogonal similarity transformation: Q**T * A * Q = H. LAPACK function  GEHRD . |
| ReflectHessenbergBalancedToQ | Generates orthogonal matrix Q  which is defined as the product of ihi-ilo elementary reflectors of order n, as returned by  ReduceToHessenbergBalanced : Q = H(ilo) H(ilo+1) . . . H(ihi-1). LAPACK function  ORGHR . |
| EigenHessenbergBalancedSchurQ | Computes the eigenvalues of a Hessenberg matrix H and the matrices T and Z from the Schur decomposition H = Z T Z**T, where T is an upper quasi-triangular matrix (the Schur form), and Z is the orthogonal matrix of Schur vectors. Optionally Z may be postmultiplied into an input orthogonal matrix Q so that this routine can give the Schur factorization of a matrix A which has been reduced to the Hessenberg form H by the orthogonal matrix Q: A = Q*H*Q**T = (QZ)*T*(QZ)**T. LAPACK function  HSEQR . |
