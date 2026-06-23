# Rank

Return matrix rank using the Gaussian method.

```
int  Rank()

```

Return Value

Rank of matrix.

Note

The rank of a system of rows (or columns) of a matrix A that has m rows and n columns is the maximum number of linearly independent rows (or columns). Several rows (columns) are called linearly independent if none of them can be expressed linearly in terms of others. The rank of the row system is always equal to the rank of the column system. This value is called the rank of the matrix.

MQL5 example:

```
  matrix a=matrix::Eye(4, 4);;
  Print("matrix a \n", a);
  Print("a.Rank()=", a.Rank());
 
  matrix I=matrix::Eye(4, 4);
  I[3, 3] = 0.;    // rank deficient matrix
  Print("I \n", I);
  Print("I.Rank()=", I.Rank());
 
  matrix b=matrix::Ones(1, 4);
  Print("b \n", b);
  Print("b.Rank()=", b.Rank());;// 1 dimension - rank 1 unless all 0
 
  matrix  zeros=matrix::Zeros(4, 1);
  Print("zeros \n", zeros);
  Print("zeros.Rank()=", zeros.Rank());
 
  /*
  matrix a
  [[1,0,0,0]
  [0,1,0,0]
  [0,0,1,0]
  [0,0,0,1]]
  a.Rank()=4
 
  I
  [[1,0,0,0]
  [0,1,0,0]
  [0,0,1,0]
  [0,0,0,0]]
  I.Rank()=3
 
  b
  [[1,1,1,1]]
  b.Rank()=1
 
  zeros
  [[0]
  [0]
  [0]
  [0]]
  zeros.Rank()=0
  */

```

Python example:

```
import numpy as np
from numpy.linalg import matrix_rank
a=(np.eye(4)) # Full rank matrix
print("a \n", a)
print("matrix_rank(a)=",matrix_rank(a))
I=np.eye(4)
I[-1,-1] = 0. # rank deficient matrix
print("I \n",I)
print("matrix_rank(I)=",matrix_rank(I))
 
b=np.ones((4,))
print("b \n",b)
print("matrix_rank(b)=",matrix_rank(b)) # 1 dimension - rank 1 unless all 0
 
zeros=np.zeros((4,))
print("zeroes \n",zeros)
print("matrix_rank(zeros)=",matrix_rank(zeros))
 
a 
 [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]
matrix_rank(a)= 4
 
I 
 [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 0.]]
matrix_rank(I)= 3
 
b 
 [1. 1. 1. 1.]
matrix_rank(b)= 1
 
zeroes 
 [0. 0. 0. 0.]
matrix_rank(zeros)= 0

```
