# Resize

Return a new matrix with a changed shape and size.

```
bool matrix::Resize(
  const ulong  rows,     // new number or rows
  const ulong  cols,     // new number or columns
  const ulong  reserve=0 // reserve amount in items
   );
 
bool vector::Resize(
  const ulong  size,     // new size.
  const ulong  reserve=0 // reserve amount in items.
   );

```

Parameters

rows

[in]  New number or rows.

cols

[in]  New number or columns.

Return Value

Returns true on success, false otherwise.

Note

The matrix (or vector) is processed in place. No copies are created. Any size can be specified, i.e., rows_new*cols_new!=rows_old*cols_old. Unlike Reshape, the matrix is processed row by row. When increasing the number of columns, the values of the extra columns are undefined. When increasing the number of rows, the values of elements in the new rows are undefined. When the number of columns is reduced, each row of the matrix is truncated.

Example

```
   matrix matrix_a={{1,2,3},{4,5,6},{7,8,9},{10,11,12}};
   Print("matrix_a\n",matrix_a);
   matrix_a.Resize(2,6);
   Print("Ressize(2,6)\n",matrix_a);
   matrix_a.Resize(3,5);
   Print("Resize(3,5)\n",matrix_a);
   matrix_a.Resize(2,4);
   Print("Resize(2,4)\n",matrix_a);
 
   /*
   matrix_a
   [[1,2,3]
    [4,5,6]
    [7,8,9]
    [10,11,12]]
   Ressize(2,6)
   [[1,2,3,4,5,6]
    [4,5,6,10,11,12]]
   Resize(3,5)
   [[1,2,3,4,5]
    [4,5,6,10,11]
    [11,12,3,8,8]]
   Resize(2,4)
   [[1,2,3,4]
    [4,5,6,10]]
   */

```
