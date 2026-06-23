# LU

LU factorization of a matrix as the product of a lower triangular matrix and an upper triangular matrix.

```
bool matrix::LU(
  matrix&  L,     // lower triangular matrix
  matrix&  U      // upper triangular matrix
   );

```

Parameters

L key

[out]  Lower triangular matrix.

U

[out]  Upper triangular matrix.

Return Value

Returns true on success, false otherwise.

Example

```
   matrix matrix_a={{1,2,3,4},
                    {5,2,6,7},
                    {8,9,3,10},
                    {11,12,14,4}};
   matrix matrix_l,matrix_u;
//--- LU decomposition
   matrix_a.LU(matrix_l,matrix_u);
   Print("matrix_l\n",matrix_l);
   Print("matrix_u\n",matrix_u);
//--- check if A = L * U
   Print("check\n",matrix_l.MatMul(matrix_u));
 
 
   /*
   matrix_l
   [[1,0,0,0]
    [5,1,0,0]
    [8,0.875,1,0]
    [11,1.25,0.5904761904761905,1]]
   matrix_u
   [[1,2,3,4]
    [0,-8,-9,-13]
    [0,0,-13.125,-10.625]
    [0,0,0,-17.47619047619047]]
   check
   [[1,2,3,4]
    [5,2,6,7]
    [8,9,3,10]
    [11,12,14,4]]
   */

```
