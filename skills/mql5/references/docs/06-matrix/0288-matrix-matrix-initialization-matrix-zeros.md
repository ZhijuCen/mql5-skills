# Zeros

This is a static function that creates and returns a new matrix filled with zeros.

```
static matrix matrix::Zeros(
  const ulong  rows,     // number of rows
  const ulong  cols      // number of columns
   );
 
static vector vector::Zeros(
  const ulong  size,     // vector size
   );
 

```

Parameters

rows

[in]  Number of rows.

cols

[in]  Number of columns.

Return Value

A new matrix of given rows and columns, filled with zeros.

MQL5 example:

```
  matrix zeros=matrix::Zeros(3, 4);
  Print("zeros = \n", zeros);
/*
zeros = 
   [[0,0,0,0]
    [0,0,0,0]
    [0,0,0,0]]
*/

```

Python example:

```
np.zeros((2, 1))
array([[ 0.],
       [ 0.]])

```
