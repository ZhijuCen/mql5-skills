# IsTrapezoidal

Check if a rectangular (not square) m-by-n matrix is upper or lower trapezoidal.

```
bool matrix::IsTrapezoidal(
  bool       is_upper      // upper or lower trapezoidal
   );

```

Parameters

is_upper

[out]  Value specifies upper or lower trapezoidal matrix is recognized.

Return Value

True if matrix is trapezoidal.

Note

Zero matrix of m-by-n size is trapezoidal.

If m < n then check whether lower triangular part under the main diagonal contains all zeros. Zero matrix of 6-by-7 size is upper trapezoidal.

If m > n then check whether upper triangular part above the main diagonal contains all zeros. Zero matrix of 7-by-6 size is lower trapezoidal.

Trapezoidal matrices

```
   upper trapezoidal               lower trapezoidal
 
   v  v  v  v  v  v  v              v  0  0  0  0  0
   0  v  v  v  v  v  v              v  v  0  0  0  0
   0  0  v  v  v  v  v              v  v  v  0  0  0
   0  0  0  v  v  v  v              v  v  v  v  0  0
   0  0  0  0  v  v  v              v  v  v  v  v  0
   0  0  0  0  0  v  v              v  v  v  v  v  v
                                    v  v  v  v  v  v
 

```
