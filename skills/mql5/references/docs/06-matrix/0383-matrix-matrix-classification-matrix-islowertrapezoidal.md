# IsLowerTrapezoidal

Check if a rectangular (not square) m-by-n matrix is lower trapezoidal.

```
bool matrix::IsLowerTrapezoidal();

```

Return Value

True if matrix is lower trapezoidal.

Note

Zero matrix of m-by-n size is lower trapezoidal.

Check if upper triangular part above the main diagonal contains all zeros.

Lower trapezoidal matrices

```
 
   v  v  0  0  0  0  0              v  0  0  0  0  0
   v  v  v  0  0  0  0              v  v  0  0  0  0
   v  v  v  v  0  0  0              v  v  v  0  0  0
   v  v  v  v  v  0  0              v  v  v  v  0  0
   v  v  v  v  v  v  0              v  v  v  v  v  0
   v  v  v  v  v  v  v              v  v  v  v  v  v
                                    v  v  v  v  v  v
 

```
