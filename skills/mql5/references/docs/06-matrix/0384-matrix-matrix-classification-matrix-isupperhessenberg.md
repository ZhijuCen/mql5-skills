# IsUpperHessenberg

Check if a square matrix is upper Hessenberg matrix.

```
bool matrix::IsUpperHessenberg();

```

Return Value

True if square matrix is upper Hessenberg matrix.

Note

Upper Hessenberg matrix contains all zeros under the subdiagonal.

Tridiagonal matrix is Hessenberg matrix. Upper triangular matrix is upper Hessenberg matrix.

Upper Hessenberg matrix

```
 
   v  v  v  v  v  v
   v  v  v  v  v  v
   0  v  v  v  v  v
   0  0  v  v  v  v
   0  0  0  v  v  v
   0  0  0  0  v  v
 

```
