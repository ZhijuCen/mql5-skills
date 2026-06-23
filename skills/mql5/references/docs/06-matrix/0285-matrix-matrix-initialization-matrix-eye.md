# Eye

A static function. Constructs a matrix having a specified size with ones on the main diagonal and zeros elsewhere. Returns a matrix with ones on the diagonal and zeros elsewhere.

```
static matrix matrix::Eye(
  const ulong  rows,        // number of rows
  const ulong  cols,        // number of columns 
  const int    ndiag=0      // index of the diagonal
   );

```

Parameters

rows

[in]  Number of rows in the output.

cols

[in]  Number of columns in the output.

ndiag=0

[in]  Index of the diagonal: 0 (the default) refers to the main diagonal, a positive value refers to an upper diagonal, and a negative value to a lower diagonal.

Return Value

A matrix where all elements are equal to zero, except for the k-th diagonal, whose values are equal to one.

MQL5 example:

```
  matrix eye=matrix::Eye(3, 3);
  Print("eye = \n", eye);
  
  eye=matrix::Eye(4, 4,1);
  Print("eye = \n", eye);  
  /*
   eye = 
   [[1,0,0]
    [0,1,0]
    [0,0,1]]
   eye = 
   [[0,1,0,0]
    [0,0,1,0]
    [0,0,0,1]
    [0,0,0,0]]   
  */

```

Python example:

```
np.eye(3, dtype=int)
array([[1, 0, 0],
       [0, 1, 0],
       [0, 0, 1]])
 
np.eye(4, k=1)
array([[0., 1., 0., 0.],
       [0., 0., 1., 0.],
       [0., 0., 0., 1.],
       [0., 0., 0., 0.]])

```
