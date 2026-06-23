# TriL

Return a copy of a matrix with elements above the k-th diagonal zeroed. Lower triangular matrix.

```
matrix matrix::Tril(
  const int     ndiag=0      // index of diagonal
   );

```

Parameters

ndiag=0

[in]  Diagonal above which to zero elements. ndiag = 0 (the default) is the main diagonal, ndiag < 0 is below it and ndiag > 0 is above.

Return Value

Array with its lower triangle filled with ones and zero elsewhere.

MQL5 example:

```
   matrix a={{1,2,3},{4,5,6},{7,8,9},{10,11,12}};
   matrix b=a.TriL(-1);
   Print("matrix b \n",b);
 
  /*
  matrix_c
  [[0,0,0]
  [4,0,0]
  [7,8,0]
  [10,11,12]]
  */

```

Python example:

```
import numpy as np
 
a=np.tril([[1,2,3],[4,5,6],[7,8,9],[10,11,12]], -1)
 
[[ 0  0  0]
 [ 4  0  0]
 [ 7  8  0]
 [10 11 12]]

```
