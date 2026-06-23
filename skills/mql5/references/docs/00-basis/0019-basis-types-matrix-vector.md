# Matrices and vectors

Type vector is a special data type in MQL5, which enables operations with vectors. A vector is a one-dimensional array of type [double](/en/docs/basis/types/double). It is one of the fundamental concepts of linear algebra, which is used in many fields of science, including physics, geometry, and others. Vectors are used to solve systems of linear equations, in 3D graphics and in other application areas. Vectors can be added and multiplied. The length or distance between vectors can be obtained through the Norm. In programming, vectors are usually represented by arrays of homogeneous elements, which may have no regular vector operations, i.e. when arrays cannot be added or multiply, and they have no norm.

Vectors can be represented as row vectors and string vectors when working with matrices. Also, vectors in linear algebra use the concepts of covariance and contravariance. These concepts do not make any difference when writing an MQL5 code, as only the programmer decides what each object of the vector type is. For example, it can be rotation, displacement or compression vector in 3D graphics.

Generally speaking, from the point of view of linear algebra, a number is also a vector, but in a one-dimensional vector space. A vector itself can be considered as a special case of a matrix.

Type matrix is another special data type in MQL5 to represent matrices. A matrix is actually a two-dimensional array of type [double](/en/docs/basis/types/double). Vectors and matrices have been introduced into MQL5 for easier operations with certain types of data sets. With them, developers can benefit from the linear algebra possibilities in a simple and math-like form. Matrices can be used to compactly write systems of linear or differential equations. The number of matrix rows corresponds to the number of equations, while the the number of columns is equal to the number of unknowns. As a result, systems of linear equations can be solved through matrix operations.

The following data types exist:

- matrix — a matrix containing double elements.
- matrixf — a matrix containing float elements.
- matrixc — a matrix containing complex elements.
- vector — a vector containing double elements.
- vectorf — a vector containing float elements.
- vectorc — a vector containing complex elements.

Template functions support notations like matrix<double>, matrix<float>, vector<double>, vector<float> instead of the corresponding types.

The following algebraic operations are defined for the matrices:

- Addition of same-size matrices
- Multiplication of suitable-size matrices: the number of columns in the left matrix must equal the number of rows in the right matrix
- Matrix multiplication by a column vector; multiplication of a row vector by a matrix according to the matrix multiplication rule. In this sense the vector is a special case of a matrix
- Matrix multiplication by a number, that is, by a scalar

Mathematics considers many different matrix types. For example, identity matrix, symmetric, skew-symmetric, upper and lower triangular matrices, and other types. Various Normal forms play an important role in the matrix theory. They represent a certain canonical form of a matrix, which can be obtained by means of certain transformations. In practice, normal forms that have additional properties, such as for example stability, are used.

The use of vectors and matrices, or rather, of special methods of the relevant types, enables the creation of simpler, briefer and clearer code, which is close to mathematical notation. With these methods, you can avoid the need to create nested loops or to mind correct indexing of arrays in calculations. Therefore, the use of these methods increases reliability and speed in developing complex programs.

## List of matrix and vector methods

Types matrix and vector include methods that correspond to the relevant [NumPy](https://numpy.org/doc/stable/reference/routines.html#) library methods. Using these methods, you can translate algorithms and codes from Python to MQL5 with minimum efforts. A lot of data processing tasks, mathematical equations, neural networks and machine learning tasks can be solved using ready-made Python methods and libraries.

| Method matrix/vector | Analogous method in NumPy | Description |
| --- | --- | --- |
| void matrix.Eye(const int rows, const int cols, const int ndiag=0) | eye | Construct a matrix with ones on the diagonal and zeros elsewhere |
| void matrix.Identity(const int rows) | identity | Construct a square matrix with ones on the main diagonal |
| void matrix.Ones(const int rows, const int cols) | ones | Construct a new matrix of given rows and columns, filled with ones |
| void matrix.Zeros(const int rows, const int cols) | zeros | Construct a new matrix of given rows and columns, filled with zeros |
| void matrix.Full(const int rows, const int cols, const scalar value) | full | Construct a new matrix of given rows and columns, filled with scalar value |
| void matrix.Copy(const matrix a) | copy | Construct a copy of the given matrix |
| void matrix.FromBuffer(const int rows, const int cols, const scalar array[], const int count=-1, const int offset=0) | frombuffer | Construct a matrix created from a 1-dimensional array |
| void matrix.FromFile(const int rows, condt int cols, const int file_handle, const int count=-1, const int offset=0) | fromfile | Construct a matrix from data in a text or binary file |
| void vector.FromString(const string source, const string sep=" ") | fromstring | Construct a vector initialized from text data in a string |
| void vector.Arange(const scalar start, const scalar stop, const scalar step=1) | arange | Construct evenly spaced values within a given interval |
| void matrix.Diag(const vector v, const int ndiag=0) | diag | Extract a diagonal or construct a diagonal matrix |
| void matrix.Tri(const int rows, const int cols, const int ndiag=0) | tri | Construct a matrix with ones at and below the given diagonal and zeros elsewhere |
| void matrix.Tril(const int rows, const int cols, const scalar array[], const int ndiag=0) | tril | Return a copy of a matrix with elements above the k-th diagonal zeroed |
| void matrix.Triu(const int rows, const int cols, const scalar array[], const int ndiag=0) | triu | Return a copy of a matrix with the elements below the k-th diagonal zeroed |
| void matrix.Vander(const vector v, const int cols=-1, const bool increasing=false) | vander | Generate a Vandermonde matrix |
| vector matrix.Row(const unsigned nrow) |  | Return a row vector |
| vector matrix.Col(const unsigned ncol) |  | Return a column vector |
| unsigned matrix.Rows() |  | Return the number of rows in a matrix |
| unsigned matrix.Cols() |  | Return the number of columns in a matrix |
| void matrix.Init() |  | Initialize a matrix |
| matrix matrix.Transpose() | transpose | Reverse or permute the axes of a matrix; returns the modified matrix |
| matrix matrix.Dot(const matrix b) | dot | Dot product of two matrices |
| matrix matrix.Inner(const matrix b) | inner | Inner product of two matrices |
| matrix matrix.Outer(const matrix b) | outer | Compute the outer product of two matrices |
| matrix matrix.MatMul(const matrix b) | matmul | Matrix product of two matrices |
| matrix matrix.MatrixPower(const int power) | matrix_power | Raise a square matrix to the (integer) power n |
| matrix matrix.Kron(const matrix b) | kron | Return Kronecker product of two matrices |
| bool matrix.Cholesky(matrix& L) | cholesky | Return the Cholesky decomposition |
| bool matrix.QR(matrix& Q, matrix& R) | qr | Compute the qr factorization of a matrix |
| bool matrix.SVD(matrix& U, matrix& V, vector& singular_values) | svd | Singular value decomposition |
| bool matrix.Eig(matrix& eigen_vectors, vector& eigen_values) | eig | Compute the eigenvalues and right eigenvectors of a square matrix |
| bool matrix.EigH(matrix& eigen_vectors, vector& eigen_values) | eigh | Return the eigenvalues and eigenvectors of a Hermitian matrix |
| bool matrix.EigVals(vector& eigen_values) | eigvals | Compute the eigenvalues of a general matrix |
| bool matrix.EigValsH(vector& eigen_values) | eigvalsh | Compute the eigenvalues of a Hermitian matrix |
| bool matrix.LU(matrix& L, matrix& U) |  | LU decomposition of a matrix as the product of a lower triangular matrix and an upper triangular matrix |
| bool matrix.LUP(matrix& L, matrix& U, matrix& P) |  | LUP decomposition with partial pivoting, which refers to LU decomposition with row permutations only: PA=LU |
| double matrix.Norm(const norm) | norm | Return matrix or vector norm |
| double matrix.Cond(const norm) | cond | Compute the condition number of a matrix |
| vector matrix.Spectrum() |  | Compute spectrum of a matrix as the set of its eigenvalues from the product AT*A |
| double matrix.Det() | det | Compute the determinant of an array |
| int matrix.Rank() | matrix_rank | Return matrix rank of array using the Gaussian method |
| int matrix.SLogDet(int& sign) | slogdet | Compute the sign and logarithm of the determinant of an array |
| double matrix.Trace() | trace | Return the sum along diagonals of the matrix |
| vector matrix.Solve(const vector b) | solve | Solve a linear matrix equation, or system of linear algebraic equations |
| vector matrix.LstSq(const vector b) | lstsq | Return the least-squares solution of linear algebraic equations (for non-square or degenerate matrices) |
| matrix matrix.Inv() | inv | Compute the (multiplicative) inverse of a matrix |
| matrix matrix.PInv() | pinv | Compute the pseudo-inverse of a matrix by the Moore-Penrose method |
| int matrix.Compare(const matrix matrix_c, const double epsilon) 
 int matrix.Compare(const matrix matrix_c, const int digits) 
 int vector.Compare(const vector vector_c, const double epsilon) 
 int vector.Compare(const vector vector_c, const int digits) |  | Compare the elements of two matrices/vectors with the specified precision |
| double matrix.Flat(const ulong index) 
 bool matrix.Flat(const ulong index,const double value) | flat | Allows addressing a matrix element through one index instead of two |
| double vector.ArgMax() 
 double matrix.ArgMax() 
 vector matrix.ArgMax(const int axis) | argmax | Return the index of the maximum value |
| double vector.ArgMin() 
 double matrix.ArgMin() 
 vector matrix.ArgMin(const int axis) | argmin | Return the index of the minimum value |
| double vector.Max() 
 double matrix.Max() 
 vector matrix.Max(const int axis) | max | Return the maximum value in a matrix/vector |
| double vector.Mean() 
 double matrix.Mean() 
 vector matrix.Mean(const int axis) | mean | Compute the arithmetic mean of element values |
| double vector.Min() 
 double matrix.Min() 
 vector matrix.Min(const int axis) | min | Return the minimum value in a matrix/vector |
| double vector.Sum() 
 double matrix.Sum() 
 vector matrix.Sum(const int axis) | sum | Return the sum of the matrix/vector elements which can also be performed for the given axis (axes). |
| void vector.Clip(const double min_value,const double max_value) 
 void matrix.Clip(const double min_value,const double max_value) | clip | Limit the elements of a matrix/vector to a specified range of valid values |
| vector vector.CumProd() 
 vector matrix.CumProd() 
 matrix matrix.CumProd(const int axis) | cumprod | Return the cumulative product of matrix/vector elements, including those along the given axis |
| vector vector.CumSum() 
 vector matrix.CumSum() 
 matrix matrix.CumSum(const int axis) | cumsum | Return the cumulative sum of matrix/vector elements, including those along the given axis |
| double vector.Prod(const double initial=1) 
 double matrix.Prod(const double initial=1) 
 vector matrix.Prod(const int axis,const double initial=1) | prod | Return the product of the matrix/vector elements which can also be performed for the given axis |
| void matrix.Reshape(const ulong rows, const ulong cols) | reshape | Change the shape of a matrix without changing its data |
| void matrix.Resize(const ulong rows,const ulong cols) | resize | Return a new matrix with a changed shape and size |
| bool matrix.SwapRows(const ulong row1, const ulong row2) |  | Swap rows in a matrix |
| bool matrix.SwapCols(const ulong col1, const ulong col2) |  | Swap columns in a matrix |
| double vector.Ptp() 
 double matrix.Ptp() 
 vector matrix.Ptp(const int axis) | ptp | Return the range of values of a matrix/vector or of the given matrix axis, equivalent to Max() - Min() |
| double vector.Percentile(const int percent) 
 double matrix.Percentile(const int percent) 
 vector matrix.Percentile(const int percent,const int axis) | percentile | Return the specified percentile of values of matrix/vector elements or elements along the specified axis. Valid values of the 'percent' parameter are in the range [0, 100] |
| double vector.Quantile(const int percent) 
 double matrix.Quantile(const int percent) 
 vector matrix.Quantile(const int percent,const int axis) | quantile | Return the specified quantile of values of matrix/vector elements or elements along the specified axis. The 'percent' parameter takes values in the range [0, 1] |
| double vector.Median() 
 double matrix.Median() 
 vector matrix.Median(const int axis) | median | Compute the median of the matrix/vector elements. The median is the middle value that separates the highest half of the array/vector elements from the lowest half of elements. |
| double vector.Average() 
 double matrix.Average() 
 vector matrix.Average(const int axis) | average | Compute the arithmetic mean of matrix/vector values. The sum of the weights in the denominator cannot be equal to 0, but some weights can be 0 |
| double vector.Std() 
 double matrix.Std() 
 vector matrix.Std(const int axis) | std | Return the standard deviation of values of matrix/vector elements or of elements along the given axis |
| double vector.Var() 
 double matrix.Var() 
 vector matrix.Var(const int axis) | var | Compute the variance of values of matrix/vector elements |
| double vector.CorrCoef(const vector& v) 
 matrix matrix.CorrCoef() | corrcoef | Compute the Pearson correlation coefficient (linear correlation coefficient). The correlation coefficient is in the range [-1, 1] |
| vector vector.Correlate(const vector& v,enum mode) | correlate | Compute the cross-correlation of two vectors. The 'mode' parameter determines the linear convolution calculation mode |
| vector vector.Convolve(const vector& v, enum mode) | convolve | Return the discrete, linear convolution of two vectors The 'mode' parameter determines the linear convolution calculation mode |
| matrix matrix.Cov() 
 matrix vector.Cov(const vector& v); (resulting matrix 2 x 2) | cov | Compute the covariance matrix. The covariance of two samples (two random variables) is a measure of their linear dependence |
