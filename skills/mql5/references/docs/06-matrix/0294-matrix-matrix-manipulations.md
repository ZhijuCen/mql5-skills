# Matrix and vector manipulations

These are methods for basic matrix operations: filling, copying, getting a part of a matrix, transposing, splitting and sorting.

There are also several methods for operations with matrix rows and columns.

| Function | Action |
| --- | --- |
| HasNan | Return the number of  NaN  values in a matrix/vector |
| ReplaceNan | Replace  NaN  values in a matrix/vector with the specified value and return the number of elements replaced |
| ReplaceToZero | Replace small values in a matrix/vector with the zero value and return the number of elements replaced |
| NormalizeDouble | Round matrix/vector elements to a specified accuracy |
| Transpose | Reverse or permute the axes of a matrix; returns the modified matrix |
| TransposeConjugate | Transposing a complex matrix with conjugation. Reverse or permute the axes of a matrix by changing a sign of an imaginary part of a complex number, return the modified matrix |
| TriL | Return a copy of a matrix with elements above the k-th diagonal zeroed. Lower triangular matrix |
| TriU | Return a copy of a matrix with elements below the k-th diagonal zeroed. Upper triangular matrix |
| Diag | Extract a diagonal or construct a diagonal matrix |
| Row | Return a row vector. Write a vector to the specified row |
| Col | Return a column vector. Write a vector to the specified column |
| Copy | Return a copy of the given matrix/vector |
| Conjugate | Changing the sign of the imaginary part of a complex number, return the modified matrix or vector |
| Concat | Concatenate 2 submatrices to one matrix. Concatenate 2 vectors to one vector |
| Compare | Compare the elements of two matrices/vectors with the specified precision |
| CompareByDigits | Compare the elements of two matrices/vectors up to significant digits |
| CompareEqual | Perform an absolute comparison of two matrices by unfolding successive rows into one-dimensional vectors |
| Flat | Allow addressing a matrix element through one index instead of two |
| Clip | Limit the elements of a matrix/vector to a specified range of valid values |
| Reshape | Change the shape of a matrix without changing its data |
| Resize | Return a new matrix with a changed shape and size |
| Set | Set the value for a vector element by the specified index |
| SwapRows | Swap rows in a matrix |
| SwapCols | Swap columns in a matrix |
| Split | Split a matrix into multiple submatrices |
| Hsplit | Split a matrix horizontally into multiple submatrices. Same as  Split  with axis=0 |
| Vsplit | Split a matrix vertically into multiple submatrices. Same as  Split  with axis=1 |
| ArgSort | Indirectly sort a matrix or vector. |
| Sort | Sort a matrix or vector in place. |
