# EigenVectorsBackward

Forms the right or left eigenvectors of a real or complex general matrix by backward transformation on the computed eigenvectors of the balanced matrix output by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance). LAPACK function [GEBAK](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gebak.html).

Computing for type matrix<double>

```
bool  matrix::EigenVectorsBackward(
   ENUM_EIG_BALANCE      job,                     // matrix balancing method
   ENUM_EIG_SIDE         side,                    // right or left eigenvectors
   long                  ilo,                     // subscript of balanced matrix
   long                  ihi,                     // superscript of balanced matrix
   vector&               scale,                   // details of permutations and scaling when balancing the input matrix
   matrix&               V                        // eigenvectors
   );

```

Computing for type matrix<float>

```
bool  matrixf::EigenVectorsBackward(
   ENUM_EIG_BALANCE      job,                     // input matrix balancing method
   ENUM_EIG_SIDE         side,                    // right or left eigenvectors
   long                  ilo,                     // subscript of balanced matrix
   long                  ihi,                     // superscript of balanced matrix
   vectorf&              scale,                   // details of permutations and scaling when balancing the input matrix
   matrixf&              V                        // eigenvectors
   );

```

Computing for type matrix<complex>

```
bool  matrixc::EigenVectorsBackward(
   ENUM_EIG_BALANCE      job,                     // input matrix balancing method
   ENUM_EIG_SIDE         side,                    // right or left eigenvectors
   long                  ilo,                     // subscript of balanced matrix
   long                  ihi,                     // superscript of balanced matrix
   vector&               scale,                   // details of permutations and scaling when balancing the input matrix
   matrixc&              V                        // eigenvectors
   );

```

Computing for type matrix<complexf>

```
bool  matrixcf::EigenVectorsBackward(
   ENUM_EIG_BALANCE      job,                     // input matrix balancing method
   ENUM_EIG_SIDE         side,                    // right or left eigenvectors
   long                  ilo,                     // subscript of balanced matrix
   long                  ihi,                     // superscript of balanced matrix
   vectorf&              scale,                   // details of permutations and scaling when balancing the input matrix
   matrixcf&             V                        // eigenvectors
   );

```

Parameters

job

[in]  Value from the ENUM_EIG_BALANCE enumeration which determines the need and method for balancing the input matrix.

side

[in]  Value from the ENUM_EIG_SIDE enumeration defining the need to compute right or left eigenvectors.

ilo

[in]  Subscript of the balanced matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

ihi

[in]  Superscript of the balanced matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

scale

[in]  Vector of details of permutations and scaling when balancing the input matrix. As returned by [MatrixBalance](/en/docs/matrix/openblas/blas_matrix_balance/matrixbalance).

V

[out]  Right or left eigenvectors backtransformed from the input eigenvectors.

Return Value

Return true if successful, otherwise false in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

When computing eigenvalues and eigenvectors, matrix balancing (scaling of rows and columns) is often used to improve numerical stability. This balancing is performed by the GEBAL function, which transforms the matrix into a "nicer" form.

After balancing and computing the eigenvectors of the transformed matrix, the result does not correspond to the original matrix. In this case, [GEBAK](https://www.intel.com/content/www/us/en/docs/onemkl/developer-reference-fortran/2025-2/gebak.html) is called to transform the eigenvectors back into the space of the original (unbalanced) matrix.

This method is applied to the matrix of right or left eigenvectors of balanced matrix. They can be produced by some [eigen solver](/en/docs/matrix/openblas/eigen_values/general_matrices).

ENUM_EIG_BALANCE

An enumeration defining the need to compute eigenvectors.

| ID | Description |
| --- | --- |
| EIGBALANCE_N | Do not diagonally scale or permute |
| EIGBALANCE_P | Perform permutations to make the matrix more nearly upper triangular. Do not diagonally scale |
| EIGBALANCE_S | Diagonally scale the matrix. Do not permute |
| EIGBALANCE_B | Both diagonally scale and permute |

ENUM_EIG_SIDE

An enumeration defining the need to compute right or left eigenvectors.

| ID | Description |
| --- | --- |
| EIGSIDE_R | 'R': right eigenvectors |
| EIGSIDE_L | 'L': left eigenvectors |
