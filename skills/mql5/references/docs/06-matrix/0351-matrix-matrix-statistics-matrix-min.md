# Min

Return the minimum value in a matrix/vector.

```
double vector::Min();
 
double matrix::Min();
 
vector matrix::Min(
  const int  axis      // axis
   );

```

Parameters

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

Return Value

Minimum value in a matrix/vector.

Example

```
   matrix matrix_a={{10,3,2},{1,8,12},{6,5,4},{7,11,9}};
   Print("matrix_a\n",matrix_a);
 
   vector cols_min=matrix_a.Min(0);
   vector rows_min=matrix_a.Min(1);
   double matrix_min=matrix_a.Min();
 
   Print("cols_min=",cols_min);
   Print("rows_min=",rows_min);
   Print("min value ",matrix_min);
 
   /*
   matrix_a
   [[10,3,2]
    [1,8,12]
    [6,5,4]
    [7,11,9]]
   cols_min=[1,3,2]
   rows_min=[2,1,4,7]
   min value 1.0
   */

```
