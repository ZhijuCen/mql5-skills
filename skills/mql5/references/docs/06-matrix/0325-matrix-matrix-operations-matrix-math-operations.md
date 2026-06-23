# Mathematical operations

Mathematical operations, including addition, subtraction, multiplication and division, can be performed on matrices and vectors element-wise.

Both matrices or both vectors must be of the same type and must have the same dimensions. Each element of the matrix operates on the corresponding element of the second matrix.

You can also use a scalar of the appropriate type (double, float or complex) as the second term (multiplier, subtrahend or divisor). In this case, each member of the matrix or vector will operate on the specified scalar.

```
  matrix matrix_a={{0.1,0.2,0.3},{0.4,0.5,0.6}};
  matrix matrix_b={{1,2,3},{4,5,6}};
 
  matrix matrix_c1=matrix_a+matrix_b;
  matrix matrix_c2=matrix_b-matrix_a;
  matrix matrix_c3=matrix_a*matrix_b;   // Hadamard product, not to be confused with matrix product! There is a special MatMul function for this
  matrix matrix_c4=matrix_b/matrix_a;
 
  matrix_c1=matrix_a+1;
  matrix_c2=matrix_b-double_value;
  matrix_c3=matrix_a*M_PI;
  matrix_c4=matrix_b/0.1;
 
//--- operations in place are possible
  matrix_a+=matrix_b;
  matrix_a/=2;

```

The same operations are available for vectors.
