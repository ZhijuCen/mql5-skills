# Copy

Create a copy of the given matrix/vector.

```
bool matrix::Copy(
  const matrix&  a     // copied matrix
   );
bool vector::Copy(
  const vector&  v     // copied vector
   );
 

```

Parameters

v

[in]  Matrix or vector to copy.

Return Value

Returns true on success, false otherwise.

MQL5 example:

```
  matrix a=matrix::Eye(3, 4);
  matrix b;
  b.Copy(a);
  matrix c=a;
  Print("matrix b \n", b);
  Print("matrix_c \n", c);
 
  /*
  /*
  matrix b
  [[1,0,0,0]
  [0,1,0,0]
  [0,0,1,0]]
  matrix_c
  [[1,0,0,0]
  [0,1,0,0]
  [0,0,1,0]]
  */
  */

```

Python example:

```
import numpy as np
 
a = np.eye(3,4)
print('a \n',a)
b = a
print('b \n',b)
c = np.copy(a)
print('c \n',c)
 
a 
 [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]]
b 
 [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]]
c 
 [[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]]

```
