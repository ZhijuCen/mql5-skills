# Full

The static function creates and returns a new matrix filled with given value.

```
static matrix matrix::Full(
  const ulong   rows,      // number or rows
  const ulong   cols,      // number of columns
  const double  value      // value to fill
   );
 
static vector vector::Full(
  const ulong   size,      // vector size
  const double  value      // value to fill
   );
 

```

Parameters

rows

[in]  Number of rows.

cols

[in]  Number of columns.

value

[in]  Value to fill all the matrix elements.

Return Value

Return a new matrix of given rows and columns, filled with specified value.

MQL5 example:

```
  matrix full=matrix::Full(3,4,10);
  Print("full = \n", full);
/*
full = 
   [[10,10,10,10]
    [10,10,10,10]
    [10,10,10,10]]
*/

```

Example

```
np.full((2, 2), 10)
array([[10, 10],
       [10, 10]])

```
