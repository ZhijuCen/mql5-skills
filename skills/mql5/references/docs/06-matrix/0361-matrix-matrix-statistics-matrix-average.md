# Average

Compute the weighted mean of matrix/vector values.

```
double vector::Average(
  const vector& weigts      // weights vector
   );
 
double matrix::Average(
  const matrix& weigts      // weights matrix
);
 
vector matrix::Average(
  const matrix& weigts,     // weights matrix
  const int     axis        // axis
   );

```

Parameters

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

Return Value

Weighted mean: scalar or vector.

Note

The weight matrix/vector is associated with the main matrix/vector.

Example

```
   matrixf matrix_a={{10,3,2},{1,8,12},{6,5,4},{7,11,9}};
   matrixf matrix_w=matrixf::Ones(4,3);
   Print("matrix_a\n",matrix_a);
 
   vectorf cols_average=matrix_a.Average(matrix_w,0);
   vectorf rows_average=matrix_a.Average(matrix_w,1);
   float matrix_average=matrix_a.Average(matrix_w);
 
   Print("cols_average ",cols_average);
   Print("rows_average ",rows_average);
   Print("average value  ",matrix_average);
 
 
   /*
   matrix_a
   [[10,3,2]
    [1,8,12]
    [6,5,4]
    [7,11,9]]
   cols_average [6,6.75,6.75]
   rows_average [5,7,5,9]
   average value  6.5
   */ value  6.5

```
