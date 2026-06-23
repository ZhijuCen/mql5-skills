# Power

Raise a square matrix to the integer power.

```
matrix matrix::Power(
  const int  power      // power
   );

```

Parameters

power

[in]  The exponent can be any integer, positive, negative, or zero.

Return Value

Matrix.

Note

The resulting matrix has the same size as the original matrix. In raised to the power of 0, the identity matrix is returned. The positive power n means that the original matrix is multiplied n times by itself. The negative power -n means that the original matrix is first inverted, and then the inverted matrix is multiplied by itself n times.

A simple algorithm for raising a matrix to a power in MQL5:

```
bool MatrixPower(matrix& c, const matrix& a, const int power)
  {
//--- matrix must be square
   if(a.Rows()!=a.Cols())
      return(false);
//--- the size of the resulting matrix is exactly the same
   ulong  rows=a.Rows();
   ulong  cols=a.Cols();
   matrix result(rows,cols);
//--- when raised to zero, return the identity matrix
   if(power==0)
      result.Identity();
   else
     {
      //--- for a negative degree, first invert the matrix
      if(power<0)
        {
         matrix inverted=a.Inv();
         result=inverted;
         for(int i=-1; i>power; i--)
            result=result.MatMul(inverted);
        }
      else
        {
         result=a;
         for(int i=1; i<power; i++)
            result=result.MatMul(a);
        }
     }
//---
   c=result;
   return(true);
  }

```

MQL5 example:

```
  matrix i= {{0, 1}, {-1, 0}};
  Print("i:\n", i);
 
  Print("i.Power(3):\n", i.Power(3));
 
  Print("i.Power(0):\n", i.Power(0));
 
  Print("i.Power(-3):\n", i.Power(-3));
 
  /*
  i:
  [[0,1]
   [-1,0]]
 
  i.Power(3):
  [[0,-1]
   [1,0]]
 
  i.Power(0):
  [[1,0]
   [0,1]]
 
  i.Power(-3):
  [[0, -1]
   [1,0]]
  */

```

Python example:

```
import numpy as np
from numpy.linalg import matrix_power
 
# matrix equiv. of the imaginary unit
i = np.array([[0, 1], [-1, 0]]) 
print("i:\n",i)
 
# should = -i
print("matrix_power(i, 3) :\n",matrix_power(i, 3) )
 
print("matrix_power(i, 0):\n",matrix_power(i, 0))
 
# should = 1/(-i) = i, but w/ f.p. elements
print("matrix_power(i, -3):\n",matrix_power(i, -3))
 
i:
 [[ 0  1]
 [-1  0]]
 
matrix_power(i, 3) :
 [[ 0 -1]
 [ 1  0]]
 
matrix_power(i, 0):
 [[1 0]
 [0 1]]
 
matrix_power(i, -3):
 [[ 0.  1.]
 [-1.  0.]]
 

```
