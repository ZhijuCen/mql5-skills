# LstSq

Return the least-squares solution of linear algebraic equations (for non-square or degenerate matrices).

```
vector matrix::LstSq(
  const vector  b      // ordinate or 'dependent variable' values
   );

```

Parameters

b

[in]  Ordinate or 'dependent variable' values. (Vector of free terms)

Return Value

Vector with solution to the system a * x = b. This is true only for systems that have an exact solution.

Example

```
   matrix a={{3, 2},
             {4,-5},
             {3, 3}};
   vector b={7,40,3};
//---
   vector x=a.LstSq(b);
//--- check, must be [5, -4]
   Print("x=", x);
//--- check, must be [7, 40, 3]
   vector b1=a.MatMul(x);
   Print("b1=",b1);
 
/*
  x=[5.000000000000002,-4]
  b1=[7.000000000000005,40.00000000000001,3.000000000000005]
*/

```
