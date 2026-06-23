# Cholesky

Compute the Cholesky decomposition.

```
bool matrix::Cholesky(
  matrix&  L      // matrix
   );

```

Parameters

L key

[out]  Lower triangular matrix.

Return Value

Returns true on success, false otherwise.

Note

Return the Cholesky decomposition, L * L.H, of the square matrix a, where L is lower-triangular and .H is the conjugate transpose operator (which is the ordinary transpose if a is real-valued). a must be Hermitian (symmetric if real-valued) and positive-definite. No checking is performed to verify whether a is Hermitian or not. In addition, only the lower-triangular and diagonal elements of a are used. Only L is actually returned.

Example

```
  matrix matrix_a= {{5.7998084, -2.1825367}, {-2.1825367, 9.85910595}};
  matrix matrix_l;
  Print("matrix_a\n", matrix_a);
 
  matrix_a.Cholesky(matrix_l);
  Print("matrix_l\n", matrix_l);
  Print("check\n", matrix_l.MatMul(matrix_l.Transpose()));
  
  /*
  matrix_a
  [[5.7998084,-2.1825367]
   [-2.1825367,9.85910595]]
  matrix_l
  [[2.408279136645086,0]
   [-0.9062640068544704,3.006291985133859]]
  check
  [[5.7998084,-2.1825367]
   [-2.1825367,9.85910595]]
  */

```
