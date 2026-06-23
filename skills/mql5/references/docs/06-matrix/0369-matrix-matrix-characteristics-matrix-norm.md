# Norm

Return matrix or vector norm.

```
double vector::Norm(
  const ENUM_VECTOR_NORM  norm,     // vector norm
  const int                        norm_p=2  // number of p-norm in case of VECTOR_NORM_P
   );
 
double matrix::Norm(
  const ENUM_MATRIX_NORM  norm      // matrix norm
   );
 

```

Parameters

norm

[in] Norm order

Return Value

Matrix or vector norm.

Note

- VECTOR_NORM_INF is the maximum absolute value among vector elements.
- VECTOR_NORM_MINUS_INF is the minimum absolute value of a vector.
- VECTOR_NORM_P is the P-norm of the vector. If norm_p=0, then this is the number of non-zero vector elements. norm_p=1 is the sum of absolute values of vector elements. norm_p=2 is the square root of the sum of squares of vector element values. The value of the norm_p parameter can be negative.
- MATRIX_NORM_FROBENIUS is the square root of the sum of the squares of the matrix element values. The Frobenius norm and the vector P2-norm are consistent.
- MATRIX_NORM_SPECTRAL is the maximum value of the matrix spectrum.
- MATRIX_NORM_NUCLEAR is the sum of the singular values of the matrix.
- MATRIX_NORM_INF is the maximum vector p1-norm among the vertical vectors of the matrix. The matrix inf-norm and the vector inf-norm are consistent.
- MATRIX_NORM_MINUS_INF is the minimum vector p1-norm among the vertical vectors of the matrix.
- MATRIX_NORM_P1 is the maximum vector p1-norm among horizontal matrix vectors.
- MATRIX_NORM_MINUS_P1 is the minimum vector p1-norm among horizontal matrix vectors.
- MATRIX_NORM_P2 is the highest singular value of the matrix.
- MATRIX_NORM_MINUS_P2 is the lowest singular value of a matrix.

A simple algorithm for calculating the P-norm of a vector in MQL5:

```
double VectorNormP(const vector& v,int norm_value)
  {
   ulong  i;
   double norm=0.0;
//---
   switch(norm_value)
     {
      case 0 :
         for(i=0; i<v.Size(); i++)
            if(v[i]!=0)
               norm+=1.0;
         break;
      case 1 :
         for(i=0; i<v.Size(); i++)
            norm+=MathAbs(v[i]);
         break;
      case 2 :
         for(i=0; i<v.Size(); i++)
            norm+=v[i]*v[i];
         norm=MathSqrt(norm);
         break;
      default :
         for(i=0; i<v.Size(); i++)
            norm+=MathPow(MathAbs(v[i]),norm_value);
         norm=MathPow(norm,1.0/norm_value);
     }
//---
   return(norm);
  }

```

MQL5 example:

```
  matrix a= {{0, 1, 2, 3, 4, 5, 6, 7, 8}};
  a=a-4;
  Print("matrix a \n", a);
  a.Reshape(3, 3);
  matrix b=a;
  Print("matrix b \n", b);
  Print("b.Norm(MATRIX_NORM_P2)=", b.Norm(MATRIX_NORM_FROBENIUS));
  Print("b.Norm(MATRIX_NORM_FROBENIUS)=", b.Norm(MATRIX_NORM_FROBENIUS));
  Print("b.Norm(MATRIX_NORM_INF)", b.Norm(MATRIX_NORM_INF));
  Print("b.Norm(MATRIX_NORM_MINUS_INF)", b.Norm(MATRIX_NORM_MINUS_INF));
  Print("b.Norm(MATRIX_NORM_P1)=)", b.Norm(MATRIX_NORM_P1));
  Print("b.Norm(MATRIX_NORM_MINUS_P1)=", b.Norm(MATRIX_NORM_MINUS_P1));
  Print("b.Norm(MATRIX_NORM_P2)=", b.Norm(MATRIX_NORM_P2));
  Print("b.Norm(MATRIX_NORM_MINUS_P2)=", b.Norm(MATRIX_NORM_MINUS_P2));
 
  /*
  matrix a
  [[-4,-3,-2,-1,0,1,2,3,4]]
  matrix b
  [[-4,-3,-2]
  [-1,0,1]
  [2,3,4]]
  b.Norm(MATRIX_NORM_P2)=7.745966692414834
  b.Norm(MATRIX_NORM_FROBENIUS)=7.745966692414834
  b.Norm(MATRIX_NORM_INF)9.0
  b.Norm(MATRIX_NORM_MINUS_INF)2.0
  b.Norm(MATRIX_NORM_P1)=)7.0
  b.Norm(MATRIX_NORM_MINUS_P1)=6.0
  b.Norm(MATRIX_NORM_P2)=7.348469228349533
  b.Norm(MATRIX_NORM_MINUS_P2)=1.857033188519056e-16
  */

```

Python example:

```
import numpy as np
from numpy import linalg as LA
a = np.arange(9) - 4
print("a \n",a)
b = a.reshape((3, 3))
print("b \n",b)
print("LA.norm(b)=",LA.norm(b))
print("LA.norm(b, 'fro')=",LA.norm(b, 'fro'))
print("LA.norm(b, np.inf)=",LA.norm(b, np.inf))
print("LA.norm(b, -np.inf)=",LA.norm(b, -np.inf))
print("LA.norm(b, 1)=",LA.norm(b, 1))
print("LA.norm(b, -1)=",LA.norm(b, -1))
print("LA.norm(b, 2)=",LA.norm(b, 2))
print("LA.norm(b, -2)=",LA.norm(b, -2))
 
a 
 [-4 -3 -2 -1  0  1  2  3  4]
b 
 [[-4 -3 -2]
 [-1  0  1]
 [ 2  3  4]]
LA.norm(b)= 7.745966692414834
LA.norm(b, 'fro')= 7.745966692414834
LA.norm(b, np.inf)= 9.0
LA.norm(b, -np.inf)= 2.0
LA.norm(b, 1)= 7.0
LA.norm(b, -1)= 6.0
LA.norm(b, 2)= 7.3484692283495345
LA.norm(b, -2)= 1.857033188519056e-16

```
