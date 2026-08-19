# FactorizationPLURaw

Computes an LU factorization of a general M-by-N matrix A using partial pivoting with row interchanges. The factorization has the form

A = P * L * U

where P is a permutation matrix, L is lower triangular with unit diagonal elements (lower trapezoidal if m > n), and U is upper triangular (upper trapezoidal if m < n). LAPACK function [GETRF](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/getrf.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationPLURaw(
   matrix&         AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<float>

```
bool  matrixf::FactorizationPLURaw(
   matrixf&        AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<complex>

```
bool  matrixc::FactorizationPLURaw(
   matrixc&        AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::FactorizationPLURaw(
   matrixcf&       AF,           // factored matrix A
   long[]&         ipiv          // pivot indices array
   );

```

Parameters

AF

[out]  Factored matrix A. The factors L and U from the factorization  A = P*L*U; the unit diagonal elements of L are not stored.

ipiv

[out]  Pivot indices array of size M; row i of the matrix A was interchanged with row  ipiv[i].

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Matrix AF and pivot indices array ipiv[] are raw output of the GETRF function and can be used for further calculations with methods [PLULinearEquationsSolution](/en/docs/matrix/openblas/factored_calculations/plulinearequationssolution), [PLUInverse](/en/docs/matrix/openblas/factored_calculations/pluinverse) and [PLUCondNumReciprocal](/en/docs/matrix/openblas/factored_calculations/plucondnumreciprocal). In these cases original matrix A must be square.
