# Var

Compute the variance of values of matrix/vector elements.

```
double vector::Var();
 
double vector::Var(
  const int  ddof      // delta degrees of freedom
);
 
double matrix::Var();
 
vector matrix::Var(
  const int  axis      // axis
);
 
vector matrix::Var(
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

Variance: scalar or vector.

Note

The variance is the average of the squared deviations from the mean, i.e., var = mean(x), where x = abs(a - a.mean())**2.

The mean is typically calculated as x.sum() / (N - ddof), where N = len(x).

Expression with ddof=0 sometimes called the “population variance”. If ddof>0 (most commonly used 1), the resulting quantity is sometimes called the “sample variance”.

Example

```
   matrixf matrix_a={{10,3,2},{1,8,12},{6,5,4},{7,11,9}};
   Print("matrix_a\n",matrix_a);
 
   vectorf cols_var=matrix_a.Var(0);
   vectorf rows_var=matrix_a.Var(1);
   float matrix_var=matrix_a.Var();
 
   Print("cols_var ",cols_var);
   Print("rows_var ",rows_var);
   Print("var value  ",matrix_var);
 
 
   /*
   matrix_a
   [[10,3,2]
    [1,8,12]
    [6,5,4]
    [7,11,9]]
   cols_var [10.5,9.1875,15.6875]
   rows_var [12.666667,20.666666,0.66666669,2.6666667]
   var value  11.916666984558105
   */

```
