# IsLowerHessenberg

Check if a square matrix is lower Hessenberg matrix.

```
bool matrix::IsLowerHessenberg();

```

Return Value

True if square matrix is lower Hessenberg matrix.

Note

Lower Hessenberg matrix contains all zeros above the superdiagonal.

Tridiagonal matrix is Hessenberg matrix. Lower triangular matrix is lower Hessenberg matrix.

Lower Hessenberg matrix

```
 
   v  v  0  0  0  0
   v  v  v  0  0  0
   v  v  v  v  0  0
   v  v  v  v  v  0
   v  v  v  v  v  v
   v  v  v  v  v  v
 

```
