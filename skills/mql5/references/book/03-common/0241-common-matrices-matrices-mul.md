# Products of matrices and vectors

Matrix multiplication is one of the basic operations in various numerical methods. For example, it is often used when implementing forward and backward propagation methods in neural network layers.

Various kinds of convolutions can also be attributed to the category of matrix products. The group of such functions in MQL5 looks like this:

- MatMul: the matrix product of two matrices
- Power: raise a square matrix to the specified integer power
- Inner: the inner product of two matrices
- Outer: the outer product of two matrices or two vector
- Kron: the Kronecker product of two matrices, a matrix and a vector, a vector and a matrix, or two vectors
- CorrCoef: calculate the Pearson correlation between rows or columns of a matrix, or between vectors
- Cov: calculate the covariance matrix of rows or columns of a matrix, or between two vectors
- Correlate: calculate the mutual correlation (cross-correlation) of two vectors
- Convolve: calculate discrete linear convolution of two vectors
- Dot: the scalar product of two vectors

To give a general idea of how to manage these methods, we will give their prototypes (in the following order: from matrix, through mixed matrix-vector, to vector).

matrix<T> matrix<T>::MatMul(const matrix<T> &m)

matrix<T> matrix<T>::Power(const int power)

matrix<T> matrix<T>::Inner(const matrix<T> &m)

matrix<T> matrix<T>::Outer(const matrix<T> &m)

matrix<T> matrix<T>::Kron(const matrix<T> &m)

matrix<T> matrix<T>::Kron(const vector<T> &v)

matrix<T> matrix<T>::CorrCoef(const bool rows = true)

matrix<T> matrix<T>::Cov(const bool rows = true)

matrix<T> vector<T>::Cov(const vector<T> &v)

T vector<T>::CorrCoef(const vector<T> &v)

vector<T> vector<T>::Correlate(const vector<T> &v, ENUM_VECTOR_CONVOLVE mode)

vector<T> vector<T>::Convolve(const vector<T> &v, ENUM_VECTOR_CONVOLVE mode)

matrix<T> vector<T>::Outer(const vector<T> &v)

matrix<T> vector<T>::Kron(const matrix<T> &m)

matrix<T> vector<T>::Kron(const vector<T> &v)

T vector<T>::Dot(const vector<T> &v)

Here is a simple example of the matrix product of two matrices using the MatMul method:

```
matrix a = {{1, 0, 0},
            {0, 1, 0}};
matrix b = {{4, 1},
            {2, 2},
            {1, 3}};
matrix c1 = a.MatMul(b);
matrix c2 = b.MatMul(a);
Print("c1 = \n", c1);
Print("c2 = \n", c2);
/*
   c1 = 
   [[4,1]
    [2,2]]
   c2 = 
   [[4,1,0]
    [2,2,0]
    [1,3,0]]
*/

```

Matrices of the form A[M,N] * B[N,K] = C[M,K] can be multiplied, i.e., the number of columns in the first matrix must be equal to the number of rows in the second matrix. If the dimensions are not consistent, the result is an empty matrix.

When multiplying a matrix and a vector, two options are allowed:

- The horizontal vector (row) is multiplied by the matrix on the right, the length of the vector is equal to the number of matrix rows
- The matrix is multiplied by a vertical vector (column) on the right, the length of the vector is equal to the number of columns of the matrix

Vectors can also be multiplied with each other. In MatMul, this is always equivalent to the dot product (the Dot method) of a row vector by a column vector, and the option when a column vector is multiplied by a row vector and a matrix is obtained is supported by another method: Outer.

Let's demonstrate the Outer product of vector v5 by vector v3, and in reverse order. In both cases, a column vector is implied on the left, and a row vector is implied on the right.

```
vector v3 = {1, 2, 3};
vector v5 = {1, 2, 3, 4, 5};
Print("v5 = \n", v5);
Print("v3 = \n", v3);
Print("v5.Outer(v3) = m[5,3] \n", v5.Outer(v3));
Print("v3.Outer(v5) = m[3,5] \n", v3.Outer(v5));
/*
   v5 =
   [1,2,3,4,5]
   v3 =
   [1,2,3]
   v5.Outer(v3) = m[5,3]
   [[1,2,3]
    [2,4,6]
    [3,6,9]
    [4,8,12]
    [5,10,15]]
   v3.Outer(v5) = m[3,5]
   [[1,2,3,4,5]
    [2,4,6,8,10]
    [3,6,9,12,15]]
*/

```
