# TriU

Return a copy of a matrix with the elements below the k-th diagonal zeroed. Upper triangular matrix.

```
matrix matrix::Triu(
  const int     ndiag=0      // index of diagonal
   );

```

Parameters

ndiag=0

[in]  Diagonal below which to zero elements. ndiag = 0 (the default) is the main diagonal, ndiag < 0 is below it and ndiag > 0 is above.

MQL5 example:

```
   matrix a={{1,2,3},{4,5,6},{7,8,9},{10,11,12}};
   matrix b=a.TriU(-1);
   Print("matrix b \n",b);
 
  /*
  matrix b
  [[1,2,3]
   [4,5,6]
   [0,8,9]
   [0,0,12]]
  */

```

Python example:

```
import numpy as np
 
a=np.triu([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
print(a)
 
[[ 1  2  3]
 [ 4  5  6]
 [ 0  8  9]
 [ 0  0 12]]

```
