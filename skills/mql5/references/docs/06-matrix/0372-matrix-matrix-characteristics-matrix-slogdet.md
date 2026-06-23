# SLogDet

Compute the sign and logarithm of a matrix determinant.

```
double matrix::SLogDet(
  int&  sign      // sign
   );

```

Parameters

sign

[out] The sign of the determinant. If the sign is even, the determinant is positive.

Return Value

A number representing the sign of the determinant.

Note

The determinant is calculated by the Gaussian method by reducing the matrix to an upper triangular form. The determinant of an upper triangular matrix is equal to the product of the main diagonal elements. The logarithm of a product is equal to the sum of the logarithms. Therefore, in case of an overflow when calculating the determinant, you can use the SLogDet method.

If the sign is even, the determinant is positive.

Example

```
 
a = np.array([[1, 2], [3, 4]])  
(sign, logdet) = np.linalg.slogdet(a)  
(sign, logdet) (-1, 0.69314718055994529) # may vary  sign * np.exp(logdet) -2.0

```
