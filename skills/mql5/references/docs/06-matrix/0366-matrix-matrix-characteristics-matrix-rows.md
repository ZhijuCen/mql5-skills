# Rows

Return the number of rows in a matrix.

```
ulong matrix::Rows()

```

Return Value

Integer.

Example

```
  matrix m= {{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}};
  m.Reshape(3, 4);
  Print("matrix m \n" , m);
  Print("m.Rows()=", m.Rows());
  Print("m.Cols()=", m.Cols());
 
  /*
   matrix m 
   [[1,2,3,4]
    [5,6,7,8]
    [9,10,11,12]]
   m.Rows()=3
   m.Cols()=4
  */

```
