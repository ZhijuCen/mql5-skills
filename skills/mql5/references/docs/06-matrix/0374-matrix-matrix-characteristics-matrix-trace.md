# Trace

Return the sum along diagonals of the matrix.

```
double matrix::Trace()

```

Return Value

The sum along the diagonal.

Note

The trace of a matrix is equal to the sum of its eigenvalues.

MQL5 example:

```
  matrix a= {{0, 1, 2, 3, 4, 5, 6, 7, 8}};
  a.Reshape(3, 3);
  Print("matrix a \n", a);
  Print("a.Trace() \n", a.Trace());
 
  /*
  matrix a
  [[0,1,2]
  [3,4,5]
  [6,7,8]]
  a.Trace()
  12.0
  */

```

Python example:

```
a = np.arange(9).reshape((3,3))
print('a \n',a)
print('np.trace(a) \n',np.trace(a))
 
a 
 [[0 1 2]
 [3 4 5]
 [6 7 8]]
 
np.trace(a) 
 12

```
