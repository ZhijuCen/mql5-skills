# Max

Return the maximum value in a matrix/vector.

```
double vector::Max();
 
double matrix::Max();
 
vector matrix::Max(
  const int  axis      // axis
   );

```

Parameters

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

Return Value

Maximum value in a matrix/vector.

Example

```
   matrix matrix_a={{10,3,2},{1,8,12},{6,5,4},{7,11,9}};
   Print("matrix_a\n",matrix_a);
 
   vector cols_max=matrix_a.Max(0);
   vector rows_max=matrix_a.Max(1);
   double matrix_max=matrix_a.Max();
 
   Print("cols_max=",cols_max);
   Print("rows_max=",rows_max);
   Print("max value ",matrix_max);
 
   /*
   matrix_a
   [[10,3,2]
    [1,8,12]
    [6,5,4]
    [7,11,9]]
   cols_max=[10,11,12]
   rows_max=[10,12,6,11]
   max value 12.0
   */  

```
