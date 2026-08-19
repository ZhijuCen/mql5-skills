# IsUpperTrapezoidal

Check if a rectangular (not square) m-by-n matrix is upper trapezoidal.

```
bool matrix::IsUpperTrapezoidal();

```

Return Value

True if matrix is upper trapezoidal.

Note

Zero matrix of m-by-n size is upper trapezoidal.

Check if lower triangular part under the main diagonal contains all zeros.

Upper trapezoidal matrices

```
 
   v  v  v  v  v  v  v              v  v  v  v  v  v
   0  v  v  v  v  v  v              v  v  v  v  v  v
   0  0  v  v  v  v  v              0  v  v  v  v  v
   0  0  0  v  v  v  v              0  0  v  v  v  v
   0  0  0  0  v  v  v              0  0  0  v  v  v
   0  0  0  0  0  v  v              0  0  0  0  v  v
                                    0  0  0  0  0  v
 

```
