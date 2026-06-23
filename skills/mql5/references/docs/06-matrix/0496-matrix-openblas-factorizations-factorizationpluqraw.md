# FactorizationPLUQRaw

Computes an LU factorization of a general N-by-N matrix A with complete pivoting (row and column interchanges). The factorization has the form

A = P * L * U * Q

where P is a rows permutation matrix, L is lower triangular with unit diagonal elements, U is upper triangular, and Q is a columns permutation matrix. LAPACK function [GETC2](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/getc2.html).

Computing for type matrix<double>

```
bool  matrix::FactorizationPLUQRaw(
   matrix&         AF,           // factored matrix A
   long[]&         ipiv,         // pivot indices array
   long[]&         jpiv          // pivot indices array
   );

```

Computing for type matrix<float>

```
bool  matrixf::FactorizationPLUQRaw(
   matrixf&        AF,           // factored matrix A
   long[]&         ipiv,         // pivot indices array
   long[]&         jpiv          // pivot indices array
   );

```

Computing for type matrix<complex>

```
bool  matrixc::FactorizationPLUQRaw(
   matrixc&        AF,           // factored matrix A
   long[]&         ipiv,         // pivot indices array
   long[]&         jpiv          // pivot indices array
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::FactorizationPLUQRaw(
   matrixcf&       AF,           // factored matrix A
   long[]&         ipiv,         // pivot indices array
   long[]&         jpiv          // pivot indices array
   );

```

Parameters

AF

[out]  Factored matrix A. The factors L and U from the factorization  A = P*L*U*Q; the unit diagonal elements of L are not stored.

ipiv

[out]  Pivot indices array of size N; row i of the matrix A was interchanged with row  ipiv[i].

jpiv

[out]  Pivot indices array of size N; column j of the matrix A was interchanged with column  jpiv[j].

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

Matrix AF and pivot indices arrays ipiv[] and jpiv[] are raw output of the GETC2 function and can be used for further calculations with method [PLUQLinearEquationsSolution](/en/docs/matrix/openblas/factored_calculations/pluqlinearequationssolution).
