# Col

Return a column vector. Write a vector to the specified column.

```
vector matrix::Col(
  const ulong   ncol      // column number
   );
 
void matrix::Col(
  const vector  v,        // column vector
  const ulong   ncol      // column number
   );

```

Parameters

ncol

[in]  Number of column.

Return Value

Vector.

Note

A column can be set for unallocated matrices (which do not have dimensions). In this case, a zero matrix will be created with the size of the vector size x column number+1, after which the values of the vector elements will be populated in the corresponding column. If the column is set to an already existing matrix, the matrix dimensions do not change and the values of the matrix elements outside the column vector do not change.

Example

```
   vector v1={1,2,3};
   matrix m1;
   m1.Col(v1,1);
   Print("m1\n",m1);
   matrix m2=matrix::Full(4,5,8);
   m2.Col(v1,2);
   Print("m2\n",m2);
   
   Print("col 1 - ",m2.Col(1));
   Print("col 2 - ",m2.Col(2));
 
  /*
  m1
  [[0,1]
  [0,2]
  [0,3]]
  m2
  [[8,8,1,8,8]
  [8,8,2,8,8]
  [8,8,3,8,8]
  [8,8,8,8,8]]
  col 1 - [8,8,8,8]
  col 2 - [1,2,3,8]
  */

```
