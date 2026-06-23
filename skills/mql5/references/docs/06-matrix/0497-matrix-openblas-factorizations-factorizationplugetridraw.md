# FactorizationPLUGeTridRaw

Computes an LU factorization of a general (non-symmetric) tridiagonal N-by-N matrix A using elimination with partial pivoting and row interchanges. The factorization has the form

A = P * L * U

where P is a permutation matrix, L is lower triangular with unit diagonal elements, and U is upper triangular. LAPACK function [GTTRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gttrf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationPLUGeTridRaw(
   matrix&         AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<float>

```
bool  matrixf::FactorizationPLUGeTridRaw(
   matrixf&        AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<complex>

```
bool  matrixc::FactorizationPLUGeTridRaw(
   matrixc&        AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::FactorizationPLUGeTridRaw(
   matrixcf&       AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Parameters

AF

[out]  Factored matrix A. The factors L and U from the factorization  A = P*L*U; the unit diagonal elements of L are not stored.

ipiv

[out]  Pivot indices array of size N; row i of the matrix A was interchanged with row  ipiv[i].

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Matrix AF and pivot indices array ipiv[] are raw output of the GTTRF function and can be used for further calculations with methods [PLUGeTridLinearEquationsSolution](/en/docs/matrix/openblas/factored_calculations/plugetridlinearequations) and [PLUGeTridCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/plugetridcondnumreciprocal).
