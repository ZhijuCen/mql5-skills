# IsTridiagonal

Check if a square matrix is tridiagonal.

```
bool matrix::IsTridiagonal();

```

Return Value

True if square matrix is tridiagonal.

Note

Tridiagonal matrix contains all zeros under the subdiagonal and above the superdiagonal.

Bidiagonal matrix upper or lower is also tridiagonal.

Tridiagonal matrix

```
 
   v  v  0  0  0  0
   v  v  v  0  0  0
   0  v  v  v  0  0
   0  0  v  v  v  0
   0  0  0  v  v  v
   0  0  0  0  v  v
 

```
