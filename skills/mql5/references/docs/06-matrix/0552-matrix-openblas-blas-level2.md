# BLAS Level 2

The BLAS Level 2 section describes functions for performing operations between matrices and vectors that implement second-level linear algebra computations — matrix–vector multiplication, linear combinations, and rank updates of matrices. These functions implement the standard procedures of the BLAS (Level 2) library and provide efficient computation for real, complex, and Hermitian matrices.

BLAS Level 2 functions are designed for:

- computing matrix–vector products;
- updating matrices (rank-1 and rank-2 modifications);
- working with specific matrix types — symmetric, Hermitian, and triangular;
- performing computations with support for different data types: float, double, complexf, and complex.

All functions return true if successful and false in case of an error.

| Function | Action |
| --- | --- |
| BlasL2GeMV | Computes a matrix-vector product using a general m-by-n matrix. y = alpha * op(A) * x + beta * y. BLAS function  GEMV . |
| BlasL2SyMV | Computes a matrix-vector product for a symmetric n-by-n matrix. y = alpha*A*x + beta*y. BLAS function  SYMV . |
| BlasL2HeMV | Computes a matrix-vector product for a Hermitian n-by-n matrix. y = alpha*A*x + beta*y. BLAS function  HEMV . |
| BlasL2TrMV | Computes a matrix-vector product using a triangular n-by-n matrix. y = op(A) * x. BLAS function  TRMV . |
| BlasL2GeR | Performs a rank-1 update of a general m-by-n matrix. AU = alpha*x*y + A. BLAS functions  GER ,  GERU . |
| BlasL2GeRC | Performs a rank-1 conjugated update of a general m-by-n matrix. AU = alpha * x * conjg(y) + A. BLAS function  GERC . |
| BlasL2SyR | Performs a rank-1 update of a symmetric n-by-n matrix. AU = alpha*x*x + A. BLAS function  SYR . |
| BlasL2HeR | Performs a rank-1 conjugated update of a Hermitian n-by-n matrix. AU = alpha * x * conjg(x) + A. BLAS function  HER2 . |
| BlasL2SyR2 | Performs a rank-2 update of a symmetric n-by-n matrix. AU = alpha*x*y + alpha*y*x + A. BLAS function  SYR2 . |
| BlasL2HeR2 | Performs a rank-2 conjugated update of a Hermitian n-by-n matrix. AU = alpha * x * conjg(y) + conjg(alpha) * y * conjg(x) + A. BLAS function  HER2 . |

### Main Function Groups

1. General Matrices

- [BlasL2GeMV](/en/docs/matrix/openblas/blas_level2/blasl2gemv) — computes a matrix–vector product: y = α·op(A)·x + β·y (BLAS GEMV)
- [BlasL2GeR](/en/docs/matrix/openblas/blas_level2/blasl2ger) — performs a rank-1 matrix update: A ← A + α·x·yᵀ (BLAS GER, GERU)
- [BlasL2GeRC](/en/docs/matrix/openblas/blas_level2/blasl2gerc) — complex variant with conjugation: A ← A + α·x·conjg(yᵀ) (BLAS GERC)

2. Symmetric Matrices (Real)

- [BlasL2SyMV](/en/docs/matrix/openblas/blas_level2/blasl2symv) — computes a matrix–vector product for a symmetric matrix: y = α·A·x + β·y (BLAS SYMV)
- [BlasL2SyR](/en/docs/matrix/openblas/blas_level2/blasl2syr) — performs a rank-1 update of a symmetric matrix: A ← A + α·x·xᵀ (BLAS SYR)
- [BlasL2SyR2](/en/docs/matrix/openblas/blas_level2/blasl2syr2) — performs a rank-2 update: A ← A + α·(x·yᵀ + y·xᵀ) (BLAS SYR2)

3. Hermitian Matrices (Complex)

- [BlasL2HeMV](/en/docs/matrix/openblas/blas_level2/blasl2hemv) — computes a matrix–vector product for a Hermitian matrix: y = α·A·x + β·y (BLAS HEMV)
- [BlasL2HeR](/en/docs/matrix/openblas/blas_level2/blasl2her) — performs a rank-1 Hermitian matrix update: A ← A + α·x·conjg(xᵀ) (BLAS HER)
- [BlasL2HeR2](/en/docs/matrix/openblas/blas_level2/blasl2her2) — performs a rank-2 Hermitian update: A ← A + α·x·conjg(yᵀ) + conjg(α)·y·conjg(xᵀ) (BLAS HER2)

4. Triangular Matrices

- [BlasL2TrMV](/en/docs/matrix/openblas/blas_level2/blasl2trmv) — computes a matrix–vector product using a triangular matrix: y = op(A)·x, where op(A) is A, Aᵀ, or Aᴴ depending on the parameter (BLAS TRMV)
