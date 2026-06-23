# Cond

Compute the condition number of a matrix.

```
double matrix::Cond(
  const ENUM_MATRIX_NORM  norm      // matrix norm
   );

```

Parameters

norm

[in]  Order of the norm from [ENUM_MATRIX_NORM](/en/docs/matrix/matrix_types/matrix_enumerations#enum_matrix_norm)

Return Value

The condition number of the matrix. May be infinite.

Note

The condition number of x is defined as the norm of x times the norm of the inverse of x [1]. The norm can be the usual L2-norm (root-of-sum-of-squares) or one of a number of other matrix norms.

The condition umber is the K value equal to the product of the matrix A norms and its inverse. Matrices with a high condition number are called ill-conditioned. Those with a low condition number are called well-conditioned. The inverse matrix is obtained using pseudo-inversion, so as not to be limited by the condition of squareness and non-singularity of the matrix.

An exception is the spectral condition number.

A simple algorithm for calculating the spectral condition number in MQL5:

```
double MatrixCondSpectral(matrix& a)
  {
   double norm=0.0;
   vector v=a.Spectrum();
 
   if(v.Size()>0)
     {
      double max_norm=v[0];
      double min_norm=v[0];
      for(ulong i=1; i<v.Size(); i++)
        {
         double real=MathAbs(v[i]);
         if(max_norm<real)
            max_norm=real;
         if(min_norm>real)
            min_norm=real;
        }
      max_norm=MathSqrt(max_norm);
      min_norm=MathSqrt(min_norm);
      if(min_norm>0.0)
         norm=max_norm/min_norm;
     }
 
   return(norm);
  }

```

MQL5 example:

```
  matrix a= {{1, 0, -1}, {0, 1, 0}, { 1, 0, 1}};
  Print("a.Cond(MATRIX_NORM_P2)=", a.Cond(MATRIX_NORM_P2));
  Print("a.Cond(MATRIX_NORM_FROBENIUS)=", a.Cond(MATRIX_NORM_FROBENIUS));
  Print("a.Cond(MATRIX_NORM_INF)=", a.Cond(MATRIX_NORM_INF));
  Print("a.Cond(MATRIX_NORM_MINUS_INF)=", a.Cond(MATRIX_NORM_MINUS_INF));
  Print("a.Cond(MATRIX_NORM_P1)=)", a.Cond(MATRIX_NORM_P1));
  Print("a.Cond(MATRIX_NORM_MINUS_P1)=", a.Cond(MATRIX_NORM_MINUS_P1));
  Print("a.Cond(MATRIX_NORM_P2)=", a.Cond(MATRIX_NORM_P2));
  Print("a.Cond(MATRIX_NORM_MINUS_P2)=", a.Cond(MATRIX_NORM_MINUS_P2));
 
  /*
  matrix a
  [[1,0,-1]
  [0,1,0]
  [1,0,1]]
  a.Cond(MATRIX_NORM_P2)=1.414213562373095
  a.Cond(MATRIX_NORM_FROBENIUS)=3.162277660168379
  a.Cond(MATRIX_NORM_INF)=2.0
  a.Cond(MATRIX_NORM_MINUS_INF)=0.9999999999999997
  a.Cond(MATRIX_NORM_P1)=)2.0
  a.Cond(MATRIX_NORM_MINUS_P1)=0.9999999999999998
  a.Cond(MATRIX_NORM_P2)=1.414213562373095
  a.Cond(MATRIX_NORM_MINUS_P2)=0.7071067811865472
  */

```

Python example:

```
import numpy as np
from numpy import linalg as LA
a = np.array([[1, 0, -1], [0, 1, 0], [1, 0, 1]])
print("a \n",a)
print("LA.cond(a)=",LA.cond(a))
print("LA.cond(a, 'fro')=",LA.cond(a, 'fro'))
print("LA.cond(a, np.inf)=",LA.cond(a, np.inf))
print("LA.cond(a, -np.inf)=",LA.cond(a, -np.inf))
print("LA.cond(a, 1)=",LA.cond(a, 1))
print("LA.cond(a, -1)=",LA.cond(a, -1))
print("LA.cond(a, 2)=",LA.cond(a, 2))
print("LA.cond(a, -2)=",LA.cond(a, -2))
 
a 
 [[ 1  0 -1]
 [ 0  1  0]
 [ 1  0  1]]
LA.cond(a)= 1.4142135623730951
LA.cond(a, 'fro')= 3.1622776601683795
LA.cond(a, np.inf)= 2.0
LA.cond(a, -np.inf)= 1.0
LA.cond(a, 1)= 2.0
LA.cond(a, -1)= 1.0
LA.cond(a, 2)= 1.4142135623730951
LA.cond(a, -2)= 0.7071067811865475

```
