# FactorizationLDLComplexSyRaw

Computes the factorization of a complex symmetric matrix A using the Bunch-Kaufman diagonal pivoting method. The form of the factorization is:

A = L * D * L**T in case of lower triangular or symmetric matrix A

or

A = U**T * D * U in case of upper triangular matrix A

where L is lower triangular with unit diagonal elements, U is upper triangular with unit diagonal elements. D is a symmetric block-diagonal matrix with 1-by-1 and 2-by-2 diagonal blocks. LAPACK function [SYTRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/sytrf.html).

Computing for type matrix<complex>

```
bool  matrixc::FactorizationLDLComplexSyRaw(
   matrixc&        AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::FactorizationLDLComplexSyRaw(
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

The input can be a symmetric, [upper triangular](/en/docs/matrix/matrix_manipulations/matrix_triu) or [lower triangular](/en/docs/matrix/matrix_manipulations/matrix_tril) matrix. Triangular matrices are assumed to be symmetric.

Matrix AF and pivot indices array ipiv[] are raw output of the SYTRF function and can be used for further calculations with methods [LDLComplexSyLinearEquationsSolution](/en/docs/matrix/openblas/factored_calculations/ldlcomplexsylinearequationssolution), [LDLComplexSyInverse](/en/docs/matrix/openblas/factored_calculations/ldlcomplexsyinverse) and [LDLComplexSyCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/ldlcomplexsycondnumreciprocal).
