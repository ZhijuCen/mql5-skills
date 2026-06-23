# Kron

Return Kronecker product of two matrices, matrix and vector, vector and matrix or two vectors.

```
matrix matrix::Kron(
  const matrix&  b      // second matrix
   );
 
matrix matrix::Kron(
  const vector&  b      // vector
   );
 
matrix vector::Kron(
  const matrix&  b      // matrix
   );
 
matrix vector::Kron(
  const vector&  b      // second vector
   );
 

```

Parameters

b

[in]  second matrix.

Return Value

Matrix.

Note

The Kronecker product is also referred to as the block matrix multiplication.

A simple algorithm for the Kronecker product for two matrices in MQL5:

```
matrix MatrixKronecker(const matrix& matrix_a,const matrix& matrix_b)
  {
   ulong  M=matrix_a.Rows();
   ulong  N=matrix_a.Cols();
   ulong  P=matrix_b.Rows();
   ulong  Q=matrix_b.Cols();
   matrix matrix_c(M*P,N*Q);
 
   for(ulong m=0; m<M; m++)
      for(ulong n=0; n<N; n++)
         for(ulong p=0; p<P; p++)
            for(ulong q=0; q<Q; q++)
               matrix_c[m*P+p][n*Q+q]=matrix_a[m][n] * matrix_b[p][q];
 
   return(matrix_c);
  }

```

MQL5 example:

```
   matrix a={{1,2,3},{4,5,6}};
   matrix b=matrix::Identity(2,2);
   vector v={1,2};
 
   Print(a.Kron(b));
   Print(a.Kron(v));
 
  /*
   [[1,0,2,0,3,0]
    [0,1,0,2,0,3]
    [4,0,5,0,6,0]
    [0,4,0,5,0,6]]
 
   [[1,2,2,4,3,6]
    [4,8,5,10,6,12]]
  */

```

Python example:

```
import numpy as np
 
A = np.arange(1,7).reshape(2,3)
B = np.identity(2)
V = [1,2]
print(np.kron(A, B))
print("")
print(np.kron(A, V))
 
[[1. 0. 2. 0. 3. 0.]
 [0. 1. 0. 2. 0. 3.]
 [4. 0. 5. 0. 6. 0.]
 [0. 4. 0. 5. 0. 6.]]
 
[[ 1  2  2  4  3  6]
 [ 4  8  5 10  6 12]]

```
