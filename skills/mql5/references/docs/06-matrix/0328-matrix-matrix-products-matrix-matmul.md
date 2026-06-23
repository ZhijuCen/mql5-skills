# MatMul

The MatMul method, which enables the multiplication of matrices and vectors, has several overloads.

Multiplying a matrix by a matrix:  matrix[M][K] * matrix[K][N] = matrix[M][N]

```
matrix  matrix::MatMul(
  const matrix&  b      // second matrix
   );

```

Multiplying a vector by a matrix:  horizontal vector[K] * matrix[K][N] = horizontal vector[N]

```
vector  vector::MatMul(
  const matrix&  b      // matrix
   );

```

Multiplying a matrix by a vector:  matrix[M][K] * vertical vector[K] = vertical vector[M]

```
vector  matrix::MatMul(
  const vector&  b      // vector
   );

```

Scalar vector multiplication:  horizontal vector * vertical vector = dot value

```
scalar  vector::MatMul(
  const vector&  b      // second vector
   );

```

Parameters

b

[in]  Matrix or vector.

Return Value

Matrix, vector, or scalar, depending on the method used.

Note

The matrices should be compatible for multiplication, i.e. the number of columns in the first matrix should be equal to the number of rows in the second matrix. Matrix multiplication is non-commutative: the result of multiplying the first matrix by the second one is not equal to the result of multiplying the second matrix by the first one in the general case.

The matrix product consists of all possible combinations of scalar products of the row vectors of the first matrix and the column vectors of the second matrix.

In scalar multiplication, vectors must have the same length.

When multiplying a vector and a matrix, the length of the vector must exactly match the number of columns in the matrix.

Naive matrix multiplication algorithm in MQL5:

```
matrix MatrixProduct(const matrix& matrix_a, const matrix& matrix_b)
  {
   matrix matrix_c;
 
   if(matrix_a.Cols()!=matrix_b.Rows())
      return(matrix_c);
      
   ulong M=matrix_a.Rows();
   ulong K=matrix_a.Cols();
   ulong N=matrix_b.Cols();
   matrix_c=matrix::Zeros(M,N);
 
   for(ulong m=0; m<M; m++)
      for(ulong k=0; k<K; k++)
         for(ulong n=0; n<N; n++)
            matrix_c[m][n]+=matrix_a[m][k]*matrix_b[k][n];
 
   return(matrix_c);
  }

```

Matrix multiplication example

```
   matrix a={{1, 0, 0},
             {0, 1, 0}};
   matrix b={{4, 1},
             {2, 2},
             {1, 3}};
   matrix c1=a.MatMul(b);
   matrix c2=b.MatMul(a);
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

An example of multiplying a horizontal vector by a matrix

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- create a 3x5 matrix
   matrix m35;
   m35.Init(3, 5, Arange);
//---
   vector v3 = {1, 2, 3};
   Print("Product of horizontal vector v and matrix m[3,5]");
   Print("On the left, vector v3 = ", v3);
   Print("On the right, matrix m35 = \n", m35);
   Print("v3.MatMul(m35) = horizontal vector v[5] \n", v3.MatMul(m35));
 
  /* Result
    Product of horizontal vector v3 and matrix m[3,5]
    On the left, vector v3 = [1,2,3]
    On the right, matrix m35 =
    [[0,1,2,3,4]
     [5,6,7,8,9]
     [10,11,12,13,14]]
    v3.MatMul(m35) = horizontal vector v[5]
    [40,46,52,58,64]
   */
  }
//+------------------------------------------------------------------+
//|  Fill the matrix with increasing values                          |
//+------------------------------------------------------------------+
void Arange(matrix & m, double start = 0, double step = 1)
  {
//---
   ulong cols = m.Cols();
   ulong rows = m.Rows();
   double value = start;
   for(ulong r = 0; r < rows; r++)
     {
      for(ulong c = 0; c < cols; c++)
        {
         m[r][c] = value;
         value += step;
        }
     }
//---
  }

```

An example of how to multiply a matrix by a vertical vector

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- create a 3x5 matrix
   matrix m35;
   m35.Init(3, 5, Arange);
//---
   Print("Product of matrix m[3,5] and vertical vector v[5]");
   vector v5 = {1,2,3,4,5};
   Print("On the left, m35 = \n",m35);
   Print("On the right v5 = ",v5);
   Print("m35.MatMul(v5) = vertical vector v[3] \n",m35.MatMul(v5));
 
  /* Result
   Product of matrix m[3,5] and vertical vector v[5]
   On the left, m35 = 
   [[0,1,2,3,4]
    [5,6,7,8,9]
    [10,11,12,13,14]]
   On the right, v5 = [1,2,3,4,5]
   m35.MatMul(v5) = vertical vector v[3] 
   [40,115,190]
   */
  }
//+------------------------------------------------------------------+
//|  Fill the matrix with increasing values                          |
//+------------------------------------------------------------------+
void Arange(matrix & m, double start = 0, double step = 1)
  {
//---
   ulong cols = m.Cols();
   ulong rows = m.Rows();
   double value = start;
   for(ulong r = 0; r < rows; r++)
     {
      for(ulong c = 0; c < cols; c++)
        {
         m[r][c] = value;
         value += step;
        }
     }
//---
  }

```

An example of scalar (dot) product of vectors

```
void OnStart()
  {
//--- scalar product of a horizontal vector and a vertical one
   vector a= {1, 2, 3};  // horizontal vector
   vector b= {4, 5, 6};  // vertical vector
   Print("a = ", a);
   Print("b = ", b);
   Print("1) a.MatMul(b) = ", a.MatMul(b));
   //--- see that the Dot method generates the same result
   Print("2) a.Dot(b) = ", a.Dot(b));
 
  /* Result
   a = [1,2,3]
   b = [4,5,6]
   1) a.MatMul(b) = 32.0
   2) a.Dot(b) = 32.0
    */
  }

```

See also

[Dot](/en/docs/matrix/matrix_products/matrix_dot), [GeMM](/en/docs/matrix/matrix_products/matrix_gemm)
