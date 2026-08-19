# MatrixBalance

Balances a general real or complex square matrix A. This involves, first, permuting A by a similarity transformation to isolate eigenvalues in the first 1 to ILO-1 and last IHI+1 to N elements on the diagonal; and second, applying a diagonal similarity transformation to rows and columns ILO to IHI to make the rows and columns as close in norm as possible.  Both steps are optional. Balancing may reduce the 1-norm of the matrix, and improve the accuracy of the computed eigenvalues and/or eigenvectors. LAPACK function [GEBAL](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gebal.html).

Computing for type matrix<double>

```
bool  matrix::MatrixBalance(
   ENUM_EIG_BALANCE      job,                     // input matrix balancing method
   matrix&               AB,                      // balanced matrix
   long&                 ilo,                     // subscript of balanced matrix
   long&                 ihi,                     // superscript of balanced matrix
   vector&               scale                    // details of permutations and scaling when balancing the input matrix
   );

```

Computing for type matrix<float>

```
bool  matrixf::MatrixBalance(
   ENUM_EIG_BALANCE      job,                     // input matrix balancing method
   matrixf&              AB,                      // balanced matrix
   long&                 ilo,                     // subscript of balanced matrix
   long&                 ihi,                     // superscript of balanced matrix
   vectorf&              scale                    // details of permutations and scaling when balancing the input matrix
   );

```

Computing for type matrix<complex>

```
bool  matrixc::MatrixBalance(
   ENUM_EIG_BALANCE      job,                     // input matrix balancing method
   matrixc&              AB,                      // balanced matrix
   long&                 ilo,                     // subscript of balanced matrix
   long&                 ihi,                     // superscript of balanced matrix
   vector&               scale                    // details of permutations and scaling when balancing the input matrix
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::MatrixBalance(
   ENUM_EIG_BALANCE      job,                     // input matrix balancing method
   matrixcf&             AB,                      // balanced matrix
   long&                 ilo,                     // subscript of balanced matrix
   long&                 ihi,                     // superscript of balanced matrix
   vectorf&              scale                    // details of permutations and scaling when balancing the input matrix
   );

```

Parameters

job

[in]  Value from the ENUM_EIG_BALANCE enumeration which determines the need and method for balancing the input matrix.

AB

[out] Balanced matrix.

ilo

[out]  Subscript of the balanced matrix.

ihi

[out]  Superscript of the balanced matrix.

scale

[out]  Vector of details of permutations and scaling when balancing the input matrix.

Details of the permutations and scaling factors applied when balancing A.

If P(j) is the index of the row and column interchanged with row and column j, and D(j) is the scaling factor applied to row and column j, then

scale(j) = P(j), for j = 1,...,ilo-1

= D(j), for j = ilo,...,ihi

= P(j) for j = ihi+1,..., n.

The order in which the interchanges are made is n to ihi+1, then 1 to ilo-1.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

ENUM_EIG_BALANCE

An enumeration defining the need to compute eigenvectors.

| ID | Description |
| --- | --- |
| EIGBALANCE_N | Do not diagonally scale or permute |
| EIGBALANCE_P | Perform permutations to make the matrix more nearly upper triangular. Do not diagonally scale |
| EIGBALANCE_S | Diagonally scale the matrix. Do not permute |
| EIGBALANCE_B | Both diagonally scale and permute |
