# Least Squares

The Least Squares section provides a set of versatile functions for solving overdetermined or underdetermined linear systems of the form A * X ≈ B using least squares methods. These functions support a variety of matrix types (float, double, complex, complexf) and implement several numerically stable algorithms based on standard LAPACK routines.

Supported Methods:

- QR / LQ factorization (LeastSquaresSolution) — the primary approach for solving systems with full-rank matrices.
- QR with compact WY representation (LeastSquaresSolutionWY) — an efficient method optimized for block operations.
- SVD-based methods (for rank-deficient matrices):
LeastSquaresSolutionDC — using a divide-and-conquer algorithm,
LeastSquaresSolutionSVD — using classical singular value decomposition.

QR with column pivoting (QR with pivoting) (LeastSquaresSolutionQRPivot) — provides robust solutions for rank-deficient systems and computes the effective rank.
Tall-Skinny QR / Short-Wide LQ (LeastSquaresSolutionQRTallSkinny) — optimized for very tall or wide matrices.

Key Features:

- Support for solving systems in various forms: with matrix A, its transpose (At), or Hermitian conjugate (AH).
- Computation of residual vectors and singular values (for SVD-based methods).
- Estimation of the effective rank of matrix A.
- Support for both single right-hand side vectors and multiple right-hand side matrices.

| Function | Action |
| --- | --- |
| LeastSquaresSolution | Solves overdetermined or underdetermined real / complex linear systems involving an m-by-n matrix A, or its transpose / conjugate-transpose, using a QR or LQ factorization of A. It is assumed that A has full rank. LAPACK function  GELS . |
| LeastSquaresSolutionDC | Computes the minimum-norm solution to a real or complex linear least squares problem: minimize 2-norm(| b - A*x |) using the singular value decomposition ( SVD ) of A. A is an m-by-n matrix which may be rank-deficient. The divide and conquer algorithm makes very mild assumptions about floating point arithmetic. LAPACK function  GELSD . |
| LeastSquaresSolutionSVD | Computes the minimum-norm solution to a real or complex linear least squares problem: minimize 2-norm(| b - A*x |) using the singular value decomposition ( SVD ) of A. A is an m-by-n matrix which may be rank-deficient. LAPACK function  GELSS . |
| LeastSquaresSolutionWY | Solves overdetermined or underdetermined real / complex linear systems involving an m-by-n matrix A, or its transpose / conjugate-transpose, using a QR or LQ factorization of A with compact WY representation of Q. It is assumed that A has full rank. LAPACK function  GELST . |
| LeastSquaresSolutionsQRPivot | Computes the minimum-norm solution to a real or complex linear least squares problem: minimize 2-norm(| b - A*x |) using a complete orthogonal factorization of A. A is an m-by-n matrix which may be rank-deficient. LAPACK function  GELSY . |
| LeastSquaresSolutionQRTallSkinny | Solves overdetermined or underdetermined real / complex linear systems involving an m-by-n matrix A, or its transpose / conjugate-transpose, using a tall skinny QR or short wide LQ factorization of A. It is assumed that A has full rank. LAPACK function  GETSLS . |
