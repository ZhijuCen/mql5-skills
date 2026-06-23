# Sum

Return the sum of the matrix/vector elements which can also be performed for the given axis (axes).

```
double vector::Sum();
 
double matrix::Sum();
 
vector matrix::Sum(
  const int  axis      // axis
   );

```

Parameters

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

Return Value

Sum of the matrix/vector elements which can also be performed for the given axis (axes).

Example

```
   matrix matrix_a={{10,3,2},{1,8,12},{6,5,4},{7,11,9}};
   Print("matrix_a\n",matrix_a);
 
   vector cols_sum=matrix_a.Sum(0);
   vector rows_sum=matrix_a.Sum(1);
   double matrix_sum=matrix_a.Sum();
 
   Print("cols_sum=",cols_sum);
   Print("rows_sum=",rows_sum);
   Print("sum value ",matrix_sum);
 
   /*
   matrix_a
   [[10,3,2]
    [1,8,12]
    [6,5,4]
    [7,11,9]]
   cols_sum=[24,27,27]
   rows_sum=[15,21,15,27]
   sum value 78.0
   */

```
