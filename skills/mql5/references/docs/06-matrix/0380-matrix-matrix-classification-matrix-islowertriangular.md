# IsLowerTriangular

Check if a square matrix is lower triangular.

```
bool matrix::IsLowerTriangular();

```

Return Value

True if square matrix is lower triangular.

Note

Zero matrix of n-by-n size is triangular. Diagonal matrix is triangular. Bidiagonal matrix is triangular.

Check if upper triangular part above the main diagonal contains all zeros.

Lower triangular matrix

```
 
   v  0  0  0  0  0
   v  v  0  0  0  0
   v  v  v  0  0  0
   v  v  v  v  0  0
   v  v  v  v  v  0
   v  v  v  v  v  v
 

```
