# Median

Compute the median of the matrix/vector elements.

```
double vector::Median();
 
double matrix::Median();
 
vector matrix::Median(
  const int  axis      // axis
   );

```

Parameters

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

Return Value

Median: scalar or vector.

Note

The median is the middle value that separates the highest half of the array/vector elements from the lowest half of elements. Same as Quantile(0.5) and Percentile(50). The correct calculation of median requires the sequence to be sorted.

Example

```
   matrixf matrix_a={{1,2,3},{4,5,6},{7,8,9},{10,11,12}};
   Print("matrix_a\n",matrix_a);
 
   vectorf cols_median=matrix_a.Median(0);
   vectorf rows_median=matrix_a.Median(1);
   float matrix_median=matrix_a.Median();
 
   Print("cols_median ",cols_median);
   Print("rows_median ",rows_median);
   Print("median value  ",matrix_median);
 
 
   /*
   matrix_a
   [[1,2,3]
    [4,5,6]
    [7,8,9]
    [10,11,12]]
   cols_median [5.5,6.5,7.5]
   rows_median [2,5,8,11]
   median value  6.5
   */
      

```
