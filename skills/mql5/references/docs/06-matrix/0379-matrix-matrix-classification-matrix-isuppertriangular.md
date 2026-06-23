# IsUpperTriangular

Check if a square matrix is upper triangular.

```
bool matrix::IsUpperTriangular();

```

Return Value

True if square matrix is upper triangular.

Note

Zero matrix of n-by-n size is triangular. Diagonal matrix is triangular. Bidiagonal matrix is triangular.

Check if lower triangular part under the main diagonal contains all zeros.

Upper triangular matrix

```
 
   v  v  v  v  v  v
   0  v  v  v  v  v
   0  0  v  v  v  v
   0  0  0  v  v  v
   0  0  0  0  v  v
   0  0  0  0  0  v
 

```
