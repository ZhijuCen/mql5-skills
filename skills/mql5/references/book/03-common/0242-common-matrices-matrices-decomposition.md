# Transformations (decomposition) of matrices

Matrix transformations are the most commonly used operations when working with data. However, many complex transformations cannot be performed analytically and with absolute accuracy.

Matrix transformations (or in other words, decompositions) are methods that decompose a matrix into its component parts, which makes it easier to calculate more complex matrix operations. Matrix decomposition methods, also called matrix factorization methods, are the basis of linear algebra algorithms, such as solving systems of linear equations and calculating the inverse of a matrix or determinant.

In particular, Singular Values Decomposition (SVD) is widely used in machine learning, which allows you to represent the original matrix as a product of three other matrices. SVD decomposition is used to solve a variety of problems, from least squares approximation to compression and image recognition.

List of available methods:

- Cholesky: calculate the Cholesky decomposition
- Eig: calculate eigenvalues and right eigenvectors of a square matrix
- Eig Vals: calculate eigenvalues of the common matrix
- LU: implement LU factorization of a matrix as a product of a lower triangular matrix and an upper triangular matrix
- LUP: implement LUP factorization with partial rotation, which is an LU factorization with row permutations only: PA=LU
- QR: implement QR factorization of the matrix
- SVD: singular value decomposition

Below are the method prototypes.

bool matrix<T>::Cholesky(matrix<T> &L)

bool matrix<T>::Eig(matrix<T> &eigen_vectors, vector<T> &eigen_values)

bool matrix<T>::EigVals(vector<T> &eigen_values)

bool matrix<T>::LU(matrix<T> &L, matrix<T> &U)

bool matrix<T>::LUP(matrix<T> &L, matrix<T> &U, matrix<T> &P)

bool matrix<T>::QR(matrix<T> &Q, matrix<T> &R)

bool matrix<T>::SVD(matrix<T> &U, matrix<T> &V, vector<T> &singular_values)

Let's show an example of a singular value decomposition using the SVD method (see. file MatrixSVD.mq5). First, we initialize the original matrix.

```
matrix a = {{0, 1, 2, 3, 4, 5, 6, 7, 8}};
a = a - 4;
a.Reshape(3, 3);
Print("matrix a \n", a);

```

Now let's make an SVD decomposition:

```
matrix U, V;
vector singular_values;
a.SVD(U, V, singular_values);
Print("U \n", U);
Print("V \n", V);
Print("singular_values = ", singular_values);

```

Let's check the expansion: the following equality must hold: U * "singular diagonal" * V = A.

```
matrix matrix_s;
matrix_s.Diag(singular_values);
Print("matrix_s \n", matrix_s);
matrix matrix_vt = V.Transpose();
Print("matrix_vt \n", matrix_vt);
matrix matrix_usvt = (U.MatMul(matrix_s)).MatMul(matrix_vt);
Print("matrix_usvt \n", matrix_usvt);

```

Let's compare the resulting and original matrix for errors.

```
ulong errors = (int)a.Compare(matrix_usvt, 1e-9);
Print("errors=", errors);

```

The log should look like this:

```
matrix a
[[-4,-3,-2]
 [-1,0,1]
 [2,3,4]]
U
[[-0.7071067811865474,0.5773502691896254,0.408248290463863]
 [-6.827109697437648e-17,0.5773502691896253,-0.8164965809277256]
 [0.7071067811865472,0.5773502691896255,0.4082482904638627]]
V
[[0.5773502691896258,-0.7071067811865474,-0.408248290463863]
 [0.5773502691896258,1.779939029415334e-16,0.8164965809277258]
 [0.5773502691896256,0.7071067811865474,-0.408248290463863]]
singular_values = [7.348469228349533,2.449489742783175,3.277709923350408e-17]
  
matrix_s
[[7.348469228349533,0,0]
 [0,2.449489742783175,0]
 [0,0,3.277709923350408e-17]]
matrix_vt
[[0.5773502691896258,0.5773502691896258,0.5773502691896256]
 [-0.7071067811865474,1.779939029415334e-16,0.7071067811865474]
 [-0.408248290463863,0.8164965809277258,-0.408248290463863]]
matrix_usvt
[[-3.999999999999997,-2.999999999999999,-2]
 [-0.9999999999999981,-5.977974170712231e-17,0.9999999999999974]
 [2,2.999999999999999,3.999999999999996]]
errors=0

```

Another practical case of applying the Convolve method is included in the example in [Machine learning methods](/en/book/common/matrices/matrices_ml).
