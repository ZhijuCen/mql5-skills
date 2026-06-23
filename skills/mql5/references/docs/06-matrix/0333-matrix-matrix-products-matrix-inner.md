# Inner

Inner product of two matrices.

```
matrix matrix::Inner(
  const matrix&  b      // second matrix
   );

```

Parameters

b

[in]  Matrix.

Return Value

Matrix.

Note

The inner product for two vectors is the dot product of the two vectors vector::Dot().

A simple algorithm for the inner product of two matrices in MQL5:

```
bool MatrixInner(matrix& c, const matrix& a, const matrix& b)
  {
//--- the number of columns must equal
   if(a.Cols()!=b.Cols())
      return(false);
//--- size of the resulting matrix depends on the number of vectors in each of the matrices
   ulong  rows=a.Rows();
   ulong  cols=b.Rows();
   matrix result(rows,cols);
//---
   for(ulong i=0; i<rows; i++)
     {
      vector v1=a.Row(i);
      for(ulong j=0; j<cols; j++)
        {
         vector v2=b.Row(j);
         result[i][j]=v1.Dot(v2);
        }
     }
//---
   c=result;
   return(true);
  }

```

MQL5 example:

```
   matrix a={{0,1,2},{3,4,5}};
   matrix b={{0,1,2},{3,4,5},{6,7,8}};
   matrix c=a.Inner(b);
   Print(c);
   matrix a1={{0,1,2}};
   matrix c1=a1.Inner(b);
   Print(c1);
 
  /*
  [[5,14,23]
  [14,50,86]]
  [[5,14,23]]
  */

```

Python example:

```
import numpy as np
 
A = np.arange(6).reshape(2, 3)
B = np.arange(9).reshape(3, 3)
A1= np.arange(3)
print(np.inner(A, B))
print("");
print(np.inner(A1, B))
 
import numpy as np
 
A = np.arange(6).reshape(2, 3)
B = np.arange(9).reshape(3, 3)
A1= np.arange(3)
print(np.inner(A, B))
print("");
print(np.inner(A1, B))

```
