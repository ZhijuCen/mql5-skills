# Transpose

Matrix transposition. Reverse or permute the axes of a matrix; returns the modified matrix.

```
matrix matrix::Transpose()

```

Return Value

Transposed matrix.

A simple matrix transposition algorithm in MQL5:

```
matrix MatrixTranspose(const matrix& matrix_a)
  {
   matrix matrix_c(matrix_a.Cols(),matrix_a.Rows());
 
   for(ulong i=0; i<matrix_c.Rows(); i++)
      for(ulong j=0; j<matrix_c.Cols(); j++)
         matrix_c[i][j]=matrix_a[j][i];
 
   return(matrix_c);
  }

```

MQL5 example:

```
  matrix a= {{0, 1, 2}, {3, 4, 5}};
  Print("matrix a \n", a);
  Print("a.Transpose() \n", a.Transpose());
 
  /*
  matrix a
  [[0,1,2]
   [3,4,5]]
  a.Transpose()
  [[0,3]
   [1,4]
   [2,5]]
  */

```

Python example:

```
import numpy as np
 
a = np.arange(6).reshape((2,3))
print("a \n",a)
print("np.transpose(a) \n",np.transpose(a))
 
a 
 [[0 1 2]
 [3 4 5]]
np.transpose(a) 
 [[0 3]
 [1 4]
 [2 5]]

```
