# Std

Return the standard deviation of values of matrix/vector elements or of elements along the given axis.

```
double vector::Std();
 
double vector::Std(
  const int  ddof      // delta degrees of freedom
);
 
double matrix::Std();
 
vector matrix::Std(
  const int  axis      // axis
);
 
vector matrix::Std(
  const int  axis,     // axis
  const int  ddof      // delta degrees of freedom
);

```

Parameters

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

ddof

[in]  “Delta Degrees of Freedom”: the divisor used in the calculation is N - ddof, where N represents the number of elements. By default ddof is zero.

Return Value

Standard_deviation: scalar or vector.

Note

The standard deviation is the square root of the average of the squared deviations from the mean, i. e., std = sqrt(mean(x)), where x = abs(a - a.mean())**2.

The average squared deviation is typically calculated as x.sum() / (N - ddof), where N = len(x).

Expression with ddof=0 sometimes called the “population standard deviation”. If ddof>0 (most commonly used 1), the resulting quantity is sometimes called the “sample standard deviation”.

Example

```
   matrixf matrix_a={{10,3,2},{1,8,12},{6,5,4},{7,11,9}};
   Print("matrix_a\n",matrix_a);
 
   vectorf cols_std=matrix_a.Std(0);
   vectorf rows_std=matrix_a.Std(1);
   float matrix_std=matrix_a.Std();
 
   Print("cols_std ",cols_std);
   Print("rows_std ",rows_std);
   Print("std value  ",matrix_std);
 
 
   /*
   matrix_a
   [[10,3,2]
    [1,8,12]
    [6,5,4]
    [7,11,9]]
   cols_std [3.2403703,3.0310888,3.9607449]
   rows_std [3.5590262,4.5460606,0.81649661,1.6329932]
   std value  3.452052593231201
   */

```
