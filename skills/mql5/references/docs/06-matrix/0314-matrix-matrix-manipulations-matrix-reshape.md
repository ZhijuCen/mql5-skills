# Reshape

Change the shape of a matrix without changing its data.

```
void  Reshape(
  const ulong  rows,     // new number or rows
  const ulong  cols      // new number or columns
   );

```

Parameters

rows

[in]  New number or rows.

cols

[in]  New number or columns.

Note

The matrix is processed in place. No copies are created. Any size can be specified, i.e., rows_new*cols_new!=rows_old*cols_old. When the matrix buffer is increased, the extra values are undefined.

Example

```
   matrix matrix_a={{1,2,3},{4,5,6},{7,8,9},{10,11,12}};
 
   Print("matrix_a\n",matrix_a);
   matrix_a.Reshape(2,6);
   Print("Reshape(2,6)\n",matrix_a);
   matrix_a.Reshape(3,5);
   Print("Reshape(3,5)\n",matrix_a);
   matrix_a.Reshape(2,4);
   Print("Reshape(2,4)\n",matrix_a);
 
  /*
  matrix_a
  [[1,2,3]
   [4,5,6]
   [7,8,9]
   [10,11,12]]
  Reshape(2,6)
  [[1,2,3,4,5,6]
   [7,8,9,10,11,12]]
  Reshape(3,5)
  [[1,2,3,4,5]
   [6,7,8,9,10]
   [11,12,0,3,0]]
  Reshape(2,4)
  [[1,2,3,4]
   [5,6,7,8]]
  */

```
