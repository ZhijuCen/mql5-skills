# Percentile

Return the specified percentile of values of matrix/vector elements or elements along the specified axis.

```
double vector::Percentile(
  const int  percent      // 
   );
 
double matrix::Percentile(
  const int  percent      // 
   );
 
vector matrix::Percentile(
  const int  percent,     // 
  const int  axis         // axis
   );

```

Parameters

percent

[in]  Percentiles to compute, which must be between 0 and 100 inclusive.

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

Return Value

Percentile: scalar or vector.

Note

Valid values of the 'percent' parameter are in the range [0, 100]. A linear algorithm is used to calculate percentiles. The correct calculation of percentiles requires the sequence to be sorted.

Example

```
   matrixf matrix_a={{1,2,3},{4,5,6},{7,8,9},{10,11,12}};
   Print("matrix_a\n",matrix_a);
 
   vectorf cols_percentile=matrix_a.Percentile(50,0);
   vectorf rows_percentile=matrix_a.Percentile(50,1);
   float matrix_percentile=matrix_a.Percentile(50);
 
   Print("cols_percentile ",cols_percentile);
   Print("rows_percentile ",rows_percentile);
   Print("percentile value  ",matrix_percentile);
 
 
   /*
   matrix_a
   [[1,2,3]
    [4,5,6]
    [7,8,9]
    [10,11,12]]
   cols_percentile [5.5,6.5,7.5]
   rows_percentile [2,5,8,11]
   percentile value  6.5
   */

```
