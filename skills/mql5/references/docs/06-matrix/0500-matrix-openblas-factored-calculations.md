# Factored Calculations

This help section describes a set of functions for the numerical solution of linear algebra problems based on matrix factorizations and LAPACK library methods, wrapped in the matrix, matrixf, matrixc, and matrixcf classes.

These functions are focused on highly efficient and reliable calculations applicable to various types of matrices: real and complex, single- and double-precision. They cover key problems of applied linear algebra, including:

- Solving systems of linear equations (SLAEs);
- Estimating the condition number of a matrix;
- Inverse transformations and computing inverse matrices;
- Special SVD-based techniques for obtaining pseudoinverses and polar decompositions.

These functions work in conjunction with matrix prefactorizations such as Cholesky, LDL, PLU, and others, implemented in the corresponding modules. The algorithms used replicate the behavior of LAPACK and allow for efficient processing of both dense and specialized matrix structures (e.g., tridiagonal).

Below are all available functions, grouped by the factorization method used.

| Function | Action |
| --- | --- |
| PLULinearEquationsSolution | Solves a system of linear equations  A * X = B,  A**T * X = B, or  A**H * X = B with an LU-factored square coefficient matrix AF computed by  FactorizationPLURaw , with multiple right-hand sides. LAPACK function  GETRS . |
| PLUInverse | Computes the inverse of an LU-factored general matrix AF computed by  FactorizationPLURaw . LAPACK function  GETRI . |
| PLUCondNumReciprocal | Estimates the reciprocal of the condition number of a general matrix A in either the one-norm or infinity-norm, using the LU factorization computed by  FactorizationPLURaw . LAPACK function  GECON . |
| PLUQLinearEquationsSolution | Solves a system of linear equations A * X = scale * RHS with a general N-by-N matrix A using the LU-factoization with complete pivoting computed by  FactorizationPLUQRaw . LAPACK function  GESC2 . |
| PLUGeTridLinearEquationsSolution | Solves a system of linear equations A * X = B,  A**T * X = B, or  A**H * X = B with a tridiagonal matrix A using the LU-factorization computed by  FactorizationPLUGeTridRaw , with multiple right-hand sides. LAPACK function  GTTRS . |
| PLUGeTridCondNumReciprocal | Estimates the reciprocal of the condition number of a general tridiagonal matrix A in either the one-norm or infinity-norm, using the LU factorization computed by  FactorizationPLUGeTridRaw . LAPACK function  GTCON . |
| LDLLinearEquationsSolution | Solves a system of linear equations  A * X = B  with a real symmetric or complex Hermitian indefinite matrix using the factorization A = U**T * D * U or A = L * D * L**T computed by  FactorizationLDLRaw , with multiple right-hand sides. LAPACK functions  SYTRS ,  HETRS . |
| LDLInverse | Computes the inverse of a real symmetric or complex Hermitian indefinite matrix using the factorization A = U**T * D * U or A = L * D * L**T computed by  FactorizationLDLRaw . LAPACK functions  SYTRI ,  HETRI . |
| LDLCondNumReciprocal | Estimates the reciprocal of the condition number of a real symmetric or complex Hermitian indefinite matrix A, using the LDLT factorization computed by  FactorizationLDLRaw . LAPACK functions  SYCON ,  HECON . |
| LDLComplexSyLinearEquationsSolution | Solves a system of linear equations  A * X = B  with a complex symmetric indefinite matrix using the factorization A = U**T * D * U or A = L * D * L**T computed by  FactorizationLDLComplexSyRaw , with multiple right-hand sides. LAPACK function  SYTRS . |
| LDLComplexSyInverse | Computes the inverse of a complex symmetric indefinite matrix using the factorization A = U**T * D * U or A = L * D * L**T computed by  FactorizationLDLComplexSyRaw . LAPACK function  SYTRI . |
| LDLComplexSyCondNumReciprocal | Estimates the reciprocal of the condition number of a complex symmetric indefinite matrix A, using the LDLT factorization computed by  FactorizationLDLComplexSyRaw . LAPACK function  SYCON . |
| LDLSyTridPDLinearEquationsSolution | Solves a system of linear equations  A * X = B  with a real symmetric or complex Hermitian positive-definite tridiagonal matrix using the factorization A = L * D * L**T computed by  FactorizationLDLSyTridPD , with multiple right-hand sides. LAPACK function  PTTRS . |
| LDLSyTridPDCondNumReciprocal | Estimates the reciprocal of the condition number of a real symmetric or complex Hermitian positive-definite tridiagonal matrix A using the LDLT factorization computed by  FactorizationLDLSyTridPD . LAPACK function  PTCON . |
| CholeskyLinearEquationsSolution | Solves a system of linear equations  A * X = B  with a real symmetric or complex Hermitian positive-definite matrix using the factorization A = L * L**T computed by  FactorizationCholesky , with multiple right-hand sides. LAPACK function  POTRS . |
| CholeskyInverse | Computes the inverse of a real symmetric or complex Hermitian positive-definite matrix using the LLT factorization computed by  FactorizationCholesky . LAPACK function  POTRI . |
| CholeskyCondNumReciprocal | Estimates the reciprocal of the condition number of a real symmetric or complex Hermitian positive-definite matrix A using the LDL factorization computed by  FactorizationCholesky . LAPACK function  POCON . |
| Pseudo Inverse | There is no special function in the OpenBLAS library to calculate the pseudo-inverse of a matrix. However, for this purpose can be used  singular value decomposition  (SVD) |
| Polar Decomposition | There is no special function in the OpenBLAS library to calculate the polar decomposition of a matrix. However, for this purpose can be used  singular value decomposition  (SVD) |

The functions provide support for various matrix types (real, complex, single-precision, and double-precision) and cover the following key tasks.

### Condition Number Estimation

Unlike the true condition number, the estimate is approximate but much faster. Here, CondNumReciprocal denotes the inverse of the condition number (i.e., 1/cond_number).

Functions of the *CondNumReciprocal type are designed to estimate the reciprocal of the condition number of a matrix:

- [CholeskyCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/choleskycondnumreciprocal) — for positive-definite matrices with LLT factorization;
- [LDLCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/ldlcondnumreciprocal) — for indefinite symmetric or Hermitian matrices with LDL factorization;
- [LDLSyTridPDCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/ldlsytridpdcondnumreciprocal) — for positive-definite symmetric tridiagonal matrices;
- [PLUCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/plucondnumreciprocal), [PLUGeTridCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/plugetridcondnumreciprocal) —  for generalized and tridiagonal matrices with LU factorization.

### Matrix Inverse

Functions of the *Inverse type calculate the inverse matrix based on the corresponding factorization:

- [CholeskyInverse](/en/docs/matrix/openblas/factored_calculations/choleskyinverse), [LDLInverse](/en/docs/matrix/openblas/factored_calculations/ldlinverse), [PLUInverse](/en/docs/matrix/openblas/factored_calculations/pluinverse) — for various forms of factorization;
- use the ipiv index array if permutation information is required.

### Linear System Solvers

*LinearEquationsSolution functions solve linear equations of the form A * X = B:

- Both matrix and vector right-hand sides are supported;
- The transposition (or Hermitian conjugation) of the coefficient matrix is taken into account via [ENUM_EQUATIONS_FORM](/en/docs/matrix/openblas/factored_calculations/plulinearequationssolution#enum_equations_form);
- Separate functions are provided for tridiagonal and generalized matrices.

### Поддержка расширенных LU-факторизаций

The [PLUQLinearEquationsSolution](/en/docs/matrix/openblas/factored_calculations/pluqlinearequationssolution) function solves the system with scaling:

```
A * X = scale * B

```

based on full LU factorization with row- and column-wise permutations.

### Special Methods (based on SVD)

While the library functions do not directly implement polar decomposition or pseudoinverse matrices, this section contains implementation examples based on singular value decomposition:

- [PolarDecomposition](/en/docs/matrix/openblas/factored_calculations/polar_decomposition) —  decomposition of A = Q * P, where Q  is an orthogonal matrix and P is a symmetric positive-definite matrix;
- [PseudoInverse](/en/docs/matrix/openblas/factored_calculations/pseudo_inverse) — calculation of the pseudoinverse of a matrix A+ = V * Σ⁺ * Uᵀ.

Notes

- All functions return true on success and false on error.
- Prerequisites include previously performed factorizations (FactorizationCholesky, FactorizationLDLRaw, GETRF, etc.).
- Calculation results may be sensitive to numerical stability, especially for small values of  rcond.
