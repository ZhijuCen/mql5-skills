# Prod

Return the product of the matrix/vector elements which can also be performed for the given axis.

```
double vector::Prod(
  const double  initial=1      // initial multiplier
   );
 
double matrix::Prod(
  const double  initial=1      // initial multiplier
   );
 
vector matrix::Prod(
  const int     axis,          // axis
  const double  initial=1      // initial multiplier
   );

```

Parameters

axis

[in]  Axis. 0 — horizontal axis, 1 — vertical axis.

initial=1

[in]  Initial multiplier.

Example

```
   matrix matrix_a={{10,3,2},{1,8,12},{6,5,4},{7,11,9}};
   Print("matrix_a\n",matrix_a);
 
   vector cols_prod=matrix_a.Prod(0);
   vector rows_prod=matrix_a.Prod(1);
   double matrix_prod=matrix_a.Prod();
 
   Print("cols_prod=",cols_prod);
   cols_prod=matrix_a.Prod(0,0.1);
   Print("cols_prod=",cols_prod);
   Print("rows_prod=",rows_prod);
   Print("prod value ",matrix_prod);
 
  /*
   matrix_a
   [[10,3,2]
    [1,8,12]
    [6,5,4]
    [7,11,9]]
   cols_prod=[420,1320,864]
   cols_prod=[42,132,86.40000000000001]
   rows_prod=[60,96,120,693]
   prod value 479001600.0
  */

```
