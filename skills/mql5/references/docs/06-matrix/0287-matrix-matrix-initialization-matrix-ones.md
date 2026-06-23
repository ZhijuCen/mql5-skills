# Ones

This is a static function that creates and returns a new matrix filled with ones.

```
static matrix matrix::Ones(
  const ulong  rows,     // number of rows
  const ulong  cols      // number of columns
   );
 
static vector vector::Ones(
  const ulong  size,     // vector size
   );
 

```

Parameters

rows

[in]  Number of rows.

cols

[in]  Number of columns.

Return Value

A new matrix of given rows and columns, filled with ones.

MQL5 example:

```
  matrix ones=matrix::Ones(4, 4);
  Print("ones = \n", ones);
/*
ones = 
   [[1,1,1,1]
    [1,1,1,1]
    [1,1,1,1]
    [1,1,1,1]]
*/

```

Python example:

```
np.ones((4, 1))
array([[1.],
       [1.]])

```
