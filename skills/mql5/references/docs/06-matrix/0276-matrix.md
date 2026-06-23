# Matrices and vectors

A matrix is a two-dimensional array of double, float, or complex numbers.

A vector is a one-dimensional array of double, float, or complex numbers. The vector has no indication of whether it is vertical or horizontal. It is determined from the use context. For example, the vector operation Dot assumes that the left vector is horizontal and the right one is vertical. If the type indication is required, one-row or one-column matrices can be used. However, this is generally not necessary.

Matrices and vectors allocate memory for data dynamically. In fact, matrices and vectors are objects that have certain properties, such as the type of data they contain and dimensions. Matrix and vector properties can be obtained using methods such as vector_a.Size(), matrix_b.Rows(), vector_c.Norm(), matrix_d.Cond() and others. Any dimension can be changed.

When creating and initializing matrices, so-called static methods are used (these are like static methods of a class). For example: matrix::Eye(), matrix::Identity(), matrix::Ones(), vector::Ones(), matrix: :Zeros(), vector::Zeros(), matrix::Full(), vector::Full(), matrix::Tri().

At the moment, matrix and vector operations do not imply the use of the complex data type, as this development direction has not yet been completed.

MQL5 supports passing of matrices and vectors to DLLs. This enables the import of functions utilizing the relevant types, from external variables.

Matrices and vectors are passed to a DLL as a pointer to a buffer. For example, to pass a matrix of type float, the corresponding parameter of the function exported from the DLL must take a float-type buffer pointer.

MQL5

```
#import "mmlib.dll"
bool sgemm(uint flags, matrix<float> &C, const matrix<float> &A, const matrix<float> &B, ulong M, ulong N, ulong K, float alpha, float beta);
#import

```

C++

```
extern "C" __declspec(dllexport) bool sgemm(UINT flags, float *C, const float *A, const float *B, UINT64 M, UINT64 N, UINT64 K, float alpha, float beta)

```

In addition to buffers, you should pass matrix and vector sizes for correct processing.

All matrix and vector methods are listed below in alphabetical order.

| Function | Action | Category |
| --- | --- | --- |
| Activation | Compute activation function values and write them to the passed vector/matrix | Machine learning |
| ArgMax | Return the index of the maximum value | Statistics |
| ArgMin | Return the index of the minimum value | Statistics |
| ArgSort | Return the sorted index | Manipulations |
| Assign | Copies a matrix, vector or array with auto cast | Initialization |
| Average | Compute the weighted average of matrix/vector values | Statistics |
| Cholesky | Compute the Cholesky decomposition | Transformations |
| Clip | Limits the elements of a matrix/vector to a given range of valid values | Manipulations |
| Col | Return a column vector. Write a vector to the specified column. | Manipulations |
| Cols | Return the number of columns in a matrix | Features |
| Compare | Compare the elements of two matrices/vectors with the specified precision | Manipulations |
| CompareByDigits | Compare the elements of two matrices/vectors with the significant figures precision | Manipulations |
| Cond | Compute the condition number of a matrix | Features |
| Convolve | Return the discrete, linear convolution of two vectors | Products |
| Copy | Return a copy of the given matrix/vector | Manipulations |
| Concat | Concatenate 2 submatrices to one matrix. Concatenate 2 vectors to one vector | Manipulations |
| CopyIndicatorBuffer | Get the data of the specified  indicator  buffer in the specified quantity to a  vector | Initialization |
| CopyRates | Gets the historical series of the  MqlRates  structure of the specified symbol-period in the specified amount into a matrix or vector | Initialization |
| CopyTicks | Get ticks from an  MqlTick  structure into a matrix or a vector | Initialization |
| CopyTicksRange | Get ticks from an  MqlTick  structure into a matrix or a vector within the specified date range | Initialization |
| CorrCoef | Compute the Pearson correlation coefficient (linear correlation coefficient) | Products |
| Correlate | Compute the cross-correlation of two vectors | Products |
| Cov | Compute the covariance matrix | Products |
| CumProd | Return the cumulative product of matrix/vector elements, including those along the given axis | Statistics |
| CumSum | Return the cumulative sum of matrix/vector elements, including those along the given axis | Statistics |
| Derivative | Compute activation function derivative values and write them to the passed vector/matrix | Machine learning |
| Det | Compute the determinant of a square invertible matrix | Features |
| Diag | Extract a diagonal or construct a diagonal matrix | Manipulations |
| Dot | Dot product of two vectors | Products |
| Eig | Computes the eigenvalues and right eigenvectors of a square matrix | Transformations |
| EigVals | Computes the eigenvalues of a general matrix | Transformations |
| Eye | Return a matrix with ones on the diagonal and zeros elsewhere | Initialization |
| Fill | Fill an existing matrix or vector with the specified value | Initialization |
| Flat | Access a matrix element through one index instead of two | Manipulations |
| Full | Create and return a new matrix filled with the given value | Initialization |
| GeMM | The GeMM (General Matrix Multiply) method implements the general multiplication of two matrices | Products |
| HasNan | Return the number of  NaN  values in a matrix/vector | Manipulations |
| Hsplit | Split a matrix horizontally into multiple submatrices. Same as Split with axis=0 | Manipulations |
| Identity | Create an identity matrix of the specified size | Initialization |
| Init | Matrix or vector initialization | Initialization |
| Inner | Inner product of two matrices | Products |
| Inv | Compute the multiplicative inverse of a square invertible matrix by the Jordan-Gauss method | Solutions |
| Kron | Return Kronecker product of two matrices, matrix and vector, vector and matrix or two vectors | Products |
| Loss | Compute loss function values and write them to the passed vector/matrix | Machine learning |
| LstSq | Return the least-squares solution of linear algebraic equations (for non-square or degenerate matrices) | Solutions |
| LU | Implement an LU decomposition of a matrix: the product of a lower triangular matrix and an upper triangular matrix | Transformations |
| LUP | Implement an LUP factorization with partial permutation, which refers to LU decomposition with row permutations only: PA=LU | Transformations |
| MatMul | Matrix product of two matrices | Products |
| Max | Return the maximum value in a matrix/vector | Statistics |
| Mean | Compute the arithmetic mean of element values | Statistics |
| Median | Compute the median of the matrix/vector elements | Statistics |
| Min | Return the minimum value in a matrix/vector | Statistics |
| Norm | Return matrix or vector norm | Features |
| Ones | Create and return a new matrix filled with ones | Initialization |
| Outer | Compute the outer product of two matrices or two vectors | Products |
| Percentile | Return the specified percentile of values of matrix/vector elements or elements along the specified axis | Statistics |
| PInv | Compute the pseudo-inverse of a matrix by the Moore-Penrose method | Solutions |
| Power | Raise a square matrix to an integer power | Products |
| Prod | Return the product of matrix/vector elements, which can also be executed for the given axis | Statistics |
| Ptp | Return the range of values of a matrix/vector or of the given matrix axis | Statistics |
| QR | Compute the qr factorization of a matrix | Transformations |
| Quantile | Return the specified quantile of values of matrix/vector elements or elements along the specified axis | Statistics |
| Random | Static function. Create and return a new matrix or vector filled with random values. Random values are generated uniformly within the specified range | Initialization |
| Rank | Return matrix rank using the Gaussian method | Features |
| RegressionMetric | Compute the regression metric as the deviation error from the regression line constructed on the specified data array | Statistics |
| Reshape | Change the shape of a matrix without changing its data | Manipulations |
| Resize | Return a new matrix with a changed shape and size | Manipulations |
| Row | Return a row vector. Write the vector to the specified row | Manipulations |
| Rows | Return the number of rows in a matrix | Features |
| Set | Sets the value for a vector element by the specified index | Manipulations |
| Size | Return the size of vector | Features |
| SLogDet | Compute the sign and logarithm of the determinant of an matrix | Features |
| Solve | Solve a linear matrix equation or a system of linear algebraic equations | Solutions |
| Sort | Sort by place | Manipulations |
| Spectrum | Compute spectrum of a matrix as the set of its eigenvalues from the product AT*A | Features |
| Split | Split a matrix into multiple submatrices | Manipulations |
| Std | Return the standard deviation of values of matrix/vector elements or elements along the specified axis | Statistics |
| Sum | Return the sum of matrix/vector elements, which can also be executed for the given axis (axes) | Statistics |
| SVD | Singular value decomposition | Transformations |
| SwapCols | Swap columns in a matrix | Manipulations |
| SwapRows | Swap rows in a matrix | Manipulations |
| Trace | Return the sum along diagonals of the matrix | Features |
| Transpose | Transpose (swap the axes) and return the modified matrix | Manipulations |
| Tri | Construct a matrix with ones on a specified diagonal and below, and zeros elsewhere | Initialization |
| TriL | Return a copy of a matrix with elements above the k-th diagonal zeroed. Lower triangular matrix | Manipulations |
| TriU | Return a copy of a matrix with the elements below the k-th diagonal zeroed. Upper triangular matrix | Manipulations |
| Var | Compute the variance of values of matrix/vector elements | Statistics |
| Vsplit | Split a matrix vertically into multiple submatrices. Same as Split with axis=1 | Manipulations |
| Zeros | Create and return a new matrix filled with zeros | Initialization |
