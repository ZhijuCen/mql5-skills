# FactorizationLDLRaw

Computes the factorization of a real symmetric or complex Hermitian matrix A using the Bunch-Kaufman diagonal pivoting method. The form of the factorization is:

A = L * D * L**T in case of lower triangular or symmetric matrix A

or

A = U**T * D * U in case of upper triangular matrix A

where L is lower triangular with unit diagonal elements, U is upper triangular with unit diagonal elements. D is a symmetric block-diagonal matrix with 1-by-1 and 2-by-2 diagonal blocks. LAPACK functions [SYTRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/sytrf.html), [HETRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/hetrf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationLDLRaw(
   matrix&         AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<float>

```
bool  matrixf::FactorizationLDLRaw(
   matrixf&        AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<complex>

```
bool  matrixc::FactorizationLDLRaw(
   matrixc&        AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::FactorizationLDLRaw(
   matrixcf&       AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Parameters

AF

[out]  Factored matrix A. The block diagonal matrix D and factor L or U.

ipiv

[out]  Pivot indices array of size N; details of the interchanges and the block structure of D.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The input can be a symmetric (Hermitian), [upper triangular](/en/docs/matrix/matrix_manipulations/matrix_triu) or [lower triangular](/en/docs/matrix/matrix_manipulations/matrix_tril) matrix. Triangular matrices are assumed to be symmetric (Hermitian conjugated).

Matrix AF and pivot indices array ipiv[] are raw output of the SYTRF (HETRF) function and can be used for further calculations with methods [LDLLinearEquationsSolution](/en/docs/matrix/openblas/factored_calculations/ldllinearequationssolution), [LDLInverse](/en/docs/matrix/openblas/factored_calculations/ldlinverse) and [LDLCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/ldlcondnumreciprocal).
