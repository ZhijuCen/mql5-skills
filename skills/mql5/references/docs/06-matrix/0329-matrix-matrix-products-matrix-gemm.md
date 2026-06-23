# GeMM

The GeMM (General Matrix Multiply) method implements the general multiplication of two matrices. The operation is defined as C ← α A B + β C , where A and B matrices can be optionally transposed. With a normal multiplication of matrices AB ([MatMul](/en/docs/matrix/matrix_products/matrix_matmul)), the alpha scalar is assumed to be equal to 1 and beta equal to zero.

The main difference between GeMM and MatMul in terms of efficiency is that MatMul always creates a new matrix/vector object, while GeMM works with an existing matrix object and does not re-create it. Therefore, when you use GeMM and pre-allocate memory for the corresponding matrix, then, while working with the same matrix sizes, there will be no memory reallocations. This can be an important advantage of GeMM for bulk computing, for example, when running optimizations in a strategy tester or when training a neural network.

Similar to MatMul, GeMM also has 4 overloads. However, the semantics of the fourth overload has been modified in order to enable the multiplication of a vertical vector with a and horizontal one.

In an existing matrix/vector object, it is not necessary to pre-allocate memory. The memory will be allocated and filled with zeros at the first GeMM call.

Multiplying a matrix by a matrix:    matrix C[M][N] = α * ( matrix A[M][K] * matrix B[K][N]) + β *  matrix C[M][N]

```
bool  matrix::GeMM(
  const matrix &A,    // first matrix
  const matrix &B,    // second matrix
  double alpha,       // alpha multiplier for product AB
  double beta,        // beta multiplier for matrix C
  uint   flags        // a combination of ENUM_GEMM values (bitwise OR), which determines whether matrices A, B and C are transposed
   );

```

Multiplying a vector by a matrix:  vector C[N] = α * ( vector A[K] * matrix B[K][N]) + β *  vector C[N]

```
bool  vector::GeMM(
  const vector &A,    // horizontal vector
  const matrix &B,    // matrix
  double alpha,       // alpha multiplier for product AB
  double beta,        // beta multiplier for vector C
  uint   flags        // ENUM_GEMM enumeration value that determines whether matrix A is transposed
   );

```

Multiplying a matrix by a vector:  vector C[M] = α * (  matrix A[M][K] * vector B[K] * ) + β *  vector C[M]

```
bool  vector::GeMM(
  const matrix &A,    // matrix
  const vector &B,    // vertical vector
  double alpha,       // alpha multiplier for product AB
  double beta,        // beta multiplier for vector C
  uint   flags        // ENUM_GEMM enumeration value that determines whether matrix B is transposed
   );

```

Multiplying a vector by a vector:  matrix C[M][N] = α * (  vector A[M] * vector B[N] * ) + β *  matrix C[M][N]. This overload returns a matrix, unlike MatMul where it returns a scalar.

```
bool  matrix::GeMM(
  const vector &A,    // first vector
  const vector &B,    // second vector
  double alpha,       // alpha multiplier for product AB
  double beta,        // beta for matrix C
  uint   flags        // ENUM_GEMM enumeration value that determines whether matrix C is transposed
   );

```

Parameters

A

[in]  Matrix or vector.

B

[in]  Matrix or vector.

alpha

[in]  Alpha multiplier for the AB product.

beta

[in]  Beta multiplier for the resulting C matrix.

flags

[in]  The ENUM_GEMM enumeration value that determines whether matrices A, B and C are transposed.

Return Value

Returns true on success or false otherwise.

ENUM_GEMM

Enumeration of flags for the GeMM method.

| ID | Description |
| --- | --- |
| TRANSP_A | Use transposed matrix A |
| TRANSP_B | Use transposed matrix B |
| TRANSP_C | Use transposed matrix C |

Note

Matrices and vectors of float, double and complex types can be used as parameters A and B. The template variants of the GeMM method are as follows:

```
bool matrix<T>::GeMM(const matrix<T> &A,const matrix<T> &B,T alpha,T beta,ulong flags);
bool matrix<T>::GeMM(const vector<T> &A,const vector<T> &B,T alpha,T beta,ulong flags);
 
bool vector<T>::GeMM(const vector<T> &A,const matrix<T> &B,T alpha,T beta,ulong flags);
bool vector<T>::GeMM(const matrix<T> &A,const vector<T> &B,T alpha,T beta,ulong flags);

```

Basically the general matrix multiplication function is described as:

```
C[m,n] = α *Sum(A[m,k]*B[k,n]) + β*C[m,n]

```

with the following sizes: matrix A is M x K, matrix B is K x N and matrix C is M x N.

Thus, the matrices should be compatible for multiplication, i.e. the number of columns in the first matrix should be equal to the number of rows in the second matrix. Matrix multiplication is non-commutative: the result of multiplying the first matrix by the second one is not equal to the result of multiplying the second matrix by the first one in the general case.

Example:

```
void OnStart()
  {
   vector vector_a= {1, 2, 3, 4, 5};
   vector vector_b= {4, 3, 2, 1};
   matrix matrix_c;
//--- calculate GeMM for two vectors
   matrix_c.GeMM(vector_a, vector_b, 1, 0);
   Print("matrix_c:\n ", matrix_c, "\n");
   /*
   matrix_c:
    [[4,3,2,1]
    [8,6,4,2]
    [12,9,6,3]
    [16,12,8,4]
    [20,15,10,5]]
   */
//--- create matrices as vectors
   matrix matrix_a(5, 1);
   matrix matrix_b(1, 4);
   matrix_a.Col(vector_a, 0);
   matrix_b.Row(vector_b, 0);
   Print("matrix_a:\n ", matrix_a);
   Print("matrix_b:\n ", matrix_b);
   /*
   matrix_a:
   [[1]
   [2]
   [3]
   [4]
   [5]]
   matrix_b:
   [[4,3,2,1]]
   */
//-- calculate GeMM for two matrices and get the same result
   matrix_c.GeMM(matrix_a, matrix_b, 1, 0);
   Print("matrix_c:\n ", matrix_c);
   /*
   matrix_c:
    [[4,3,2,1]
    [8,6,4,2]
    [12,9,6,3]
    [16,12,8,4]
    [20,15,10,5]]
   */
  }

```

See also

[MatMul](/en/docs/matrix/matrix_products/matrix_matmul)
