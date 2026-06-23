# Det

Compute the determinant of a square invertible matrix.

```
double matrix::Det()

```

Return Value

Determinant of matrix.

Note

2nd and 3rd order matrix determinants are calculated according to the Sarrus rule. d2=a11*a22-a12*a21; d3=a11*a22*a33+a12*a23*a31+a13*a21*a32-a13*a22*a31-a11*a23*a32-a12*a21*a33

The determinant is calculated by the Gaussian method by reducing the matrix to an upper triangular form. The determinant of an upper triangular matrix is equal to the product of the main diagonal elements.

If at least one matrix row or column is zero, the determinant is zero.

If two or more matrix rows or columns are linearly dependent, its determinant is zero.

The determinant of a matrix is equal to the product of its eigenvalues.

MQL5 example:

```
   matrix m={{1,2},{3,4}};
   double det=m.Det();
   Print("matrix m\n",m);
   Print("det(m)=",det);
   /*
   matrix m
   [[1,2]
    [3,4]]
   det(m)=-2.0      
   */

```

Python example:

```
import numpy as np
 
a = np.array([[1, 2], [3, 4]])
print('a \n',a)
print('nnp.linalg.det(a) \n',np.linalg.det(a))
 
a 
 [[1 2]
 [3 4]]
 
np.linalg.det(a) 
 -2.0000000000000004

```
