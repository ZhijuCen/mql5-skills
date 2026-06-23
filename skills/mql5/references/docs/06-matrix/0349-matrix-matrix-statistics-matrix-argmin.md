# ArgMin

Return the index of the minimum value.

```
ulong vector::ArgMin();
 
ulong matrix::ArgMin();
 
vector matrix::ArgMin(
  const int  axis      // axis
   );

```

Parameters

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

Return Value

Index of the minimum value.

Example

```
   matrix matrix_a={{10,3,2},{1,8,12},{6,5,4},{7,11,9}};
   Print("matrix_a\n",matrix_a);
 
   vector cols_min=matrix_a.ArgMin(0);
   vector rows_min=matrix_a.ArgMin(1);
   ulong  matrix_min=matrix_a.ArgMin();
 
   Print("cols_min=",cols_min);
   Print("rows_min=",rows_min);
   Print("min index ",matrix_min,"  min value ",matrix_a.Flat(matrix_min));
 
   /*
   matrix_a
   [[10,3,2]
    [1,8,12]
    [6,5,4]
    [7,11,9]]
   cols_min=[1,0,0]
   rows_min=[2,0,2,0]
   min index 3  min value 1.0
   */

```
