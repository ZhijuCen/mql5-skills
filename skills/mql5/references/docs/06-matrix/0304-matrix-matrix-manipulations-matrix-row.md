# Row

Return a row vector. Write a vector to the specified row

```
vector matrix::Row(
  const ulong   nrow      // row number
   );
 
void matrix::Row(
  const vector  v,        // row vector
  const ulong   nrow      // row number
   );
 

```

Parameters

nrow

[in]  Number of row.

Return Value

Vector.

Note

A row can be set for unallocated matrices (which do not have dimensions). In this case, a zero matrix will be created with the size of the vector size x row number+1, after which the values of the vector elements will be populated in the corresponding row. If the row is set to an already existing matrix, the matrix dimensions do not change and the values of the matrix elements outside the row vector do not change.

Example

```
   vector v1={1,2,3};
   matrix m1;
   m1.Row(v1,1);
   Print("m1\n",m1);
   matrix m2=matrix::Full(4,5,7);
   m2.Row(v1,2);
   Print("m2\n",m2);
   
   Print("row 1 - ",m2.Row(1));
   Print("row 2 - ",m2.Row(2));
 
  /*
  m1
  [[0,0,0]
  [1,2,3]]
  m2
  [[7,7,7,7,7]
  [7,7,7,7,7]
  [1,2,3,7,7]
  [7,7,7,7,7]]
  row 1 - [7,7,7,7,7]
  row 2 - [1,2,3,7,7]
  */

```
