# Dot

Dot product of two vectors.

```
double vector::Dot(
  const vector&  b      // second vector
   );

```

Parameters

b

[in]  Vector.

Return Value

Scalar.

Note

The dot product of two matrices is the matrix product matrix::MatMul().

A simple algorithm for the scalar product of vectors in MQL5:

```
double VectorDot(const vector& vector_a, const vector& vector_b)
  {
   double dot=0;
 
   if(vector_a.Size()==vector_b.Size())
     {
      for(ulong i=0; i<vector_a.Size(); i++)
         dot+=vector_a[i]*vector_b[i];
     }
 
   return(dot);
  }

```

MQL5 example:

```
   for(ulong i=0; i<rows; i++)
     {
      vector v1=a.Row(i);
      for(ulong j=0; j<cols; j++)
        {
         vector v2=b.Row(j);
         result[i][j]=v1.Dot(v2);
        }
     }

```

Python example:

```
import numpy as np
 
a = [1, 0, 0, 1]
b = [4, 1, 2, 2]
print(np.dot(a, b))
 
>>> 6

```
