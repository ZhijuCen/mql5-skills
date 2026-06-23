# Tri

This is a static function Construct a matrix with ones at and below the given diagonal and zeros elsewhere.

```
static matrix matrix::Tri(
  const ulong rows,        // number of rows
  const ulong cols,        // number of columns
  const int   ndiag=0      // number of diagonal
   );

```

Parameters

rows

[in]  Number of rows in the array.

cols

[in]  Number of columns in the array.

ndiag=0

[in]  The sub-diagonal at and below which the array is filled. k = 0 is the main diagonal, while k < 0 is below it, and k > 0 is above. The default is 0.

Return Value

Array with its lower triangle filled with ones and zero elsewhere.

MQL5 example:

```
   matrix matrix_a=matrix::Tri(3,4,1);
   Print("Tri(3,4,1)\n",matrix_a);
   matrix_a=matrix::Tri(4,3,-1);
   Print("Tri(4,3,-1)\n",matrix_a);
 
/*
   Tri(3,4,1)
   [[1,1,0,0]
    [1,1,1,0]
    [1,1,1,1]]
   Tri(4,3,-1)
   [[0,0,0]
    [1,0,0]
    [1,1,0]
    [1,1,1]]
*/

```

Example

```
np.tri(3, 5, 2, dtype=int)
array([[1, 1, 1, 0, 0],
       [1, 1, 1, 1, 0],
       [1, 1, 1, 1, 1]])

```
