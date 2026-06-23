# Concat

Concatenate 2 submatrices to one matrix. Concatenate 2 vectors to one vector.

```
vector vector::Concat(
  const vector&  second_part      // second vector to concatenate
   );
 
vector matrix::Concat(
  const matrix&  second_part      // second matrix to concatenate
   );
 
matrix matrix::Split(
  const matrix&  second_part,     // second matrix to concatenate
  const int      axis             // axis
   );

```

Parameters

second_part

[in] Second vector or matrix to concatenate. If matrices are concatenated along any of the axes, then the sizes of the matrices must be consistent according to the axis.

axis

[in]  Axis. 0 - horizontal axis, 1 - vertical axis.

Return Value

Returns vector if vectors or matrices concatenated without axis parameter, or matrix concatenated along horizontal or vertical axis.

Example

```
   vector vector_a={1,2,3,4};
   vector vector_b={5,6,7};
   vector vector_c=vector_a.Concat(vector_b);
   Print("vector_c=",vector_c);
 
   matrix matrix_a={{1,2,3},{4,5,6}};
   matrix matrix_b={{7,8,9},{10,11,12}};
   vector_c=matrix_a.Concat(matrix_b);
   Print("vector_c=",vector_c);
 
   matrix matrix_c0=matrix_a.Concat(matrix_b,0);
   Print("matrix_c0=\n",matrix_c0);
 
   matrix matrix_c1=matrix_a.Concat(matrix_b,1);
   Print("matrix_c1=\n",matrix_c1);
 
  /*
  vector_c=[1,2,3,4,5,6,7]
  vector_c=[1,2,3,4,5,6,7,8,9,10,11,12]
  matrix_c0=
  [[1,2,3]
   [4,5,6]
   [7,8,9]
   [10,11,12]]
  matrix_c1=
  [[1,2,3,7,8,9]
   [4,5,6,10,11,12]]
  */

```
