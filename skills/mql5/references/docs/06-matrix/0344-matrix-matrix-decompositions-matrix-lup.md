# LUP

LUP factorization with partial pivoting, which refers to LU decomposition with row permutations only: PA=LU.

```
bool  LUP(
  matrix&  L,     // lower triangular matrix
  matrix&  U,     // upper triangular matrix
  matrix&  P      // permutations matrix
   );

```

Parameters

L key

[out]  Lower triangular matrix.

U

[out]  Upper triangular matrix.

P

[out]  Permutations matrix

Return Value

Returns true on success, false otherwise.

Example

```
   matrix matrix_a={{1,2,3,4},
                    {5,2,6,7},
                    {8,9,3,10},
                    {11,12,14,4}};
   matrix matrix_l,matrix_u,matrix_p;
//--- LUP decomposition
   matrix_a.LUP(matrix_l,matrix_u,matrix_p);
   Print("matrix_l\n",matrix_l);
   Print("matrix_u\n",matrix_u);
   Print("matrix_p\n",matrix_p);
//--- check if P * A = L * U
   Print("P * A\n",matrix_p.MatMul(matrix_a));
   Print("L * U\n",matrix_l.MatMul(matrix_u));
 
   /*
   matrix_l
   [[1,0,0,0]
    [0.4545454545454545,1,0,0]
    [0.7272727272727273,-0.07894736842105282,1,0]
    [0.09090909090909091,-0.2631578947368421,-0.2262773722627738,1]]
   matrix_u
   [[11,12,14,4]
    [0,-3.454545454545454,-0.3636363636363633,5.181818181818182]
    [0,0,-7.210526315789473,7.500000000000001]
    [0,0,0,6.697080291970803]]
   matrix_p
   [[0,0,0,1]
    [0,1,0,0]
    [0,0,1,0]
    [1,0,0,0]]
   P * A
   [[11,12,14,4]
    [5,2,6,7]
    [8,9,3,10]
    [1,2,3,4]]
   L * U
   [[11,12,14,4]
    [5,2,6,7]
    [8,9,3.000000000000001,10]
    [1,2,3,4]]
   */

```
