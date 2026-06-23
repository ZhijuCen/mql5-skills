# PInv

Compute the pseudo-inverse of a matrix by the Moore-Penrose method.

```
matrix matrix::PInv()

```

Return Value

The pseudo-inverse of matrix.

Example

```
int TestPseudoInverse(const int size_m, const int size_k)
  {
   matrix matrix_a(size_m,size_k);
   matrix matrix_inverted(size_k,size_m);
   matrix matrix_temp;
   matrix matrix_a2;
//--- fill the matrix
   MatrixTestFirst(matrix_a);
//--- invert
   matrix_inverted=matrix_a.PInv();
//--- check the correctness
   int errors=0;
//--- A * A+ * A = A   (A+ is a pseudo-inverse of A)
   matrix_temp=matrix_a.MatMul(matrix_inverted);
   matrix_a2=matrix_temp.MatMul(matrix_a);
   errors=(int)matrix_a.CompareByDigits(matrix_a2,10);
 
   printf("PseudoInversion %s matrix_size  %d x %d  errors=%d",errors==0?"passed":"failed",size_m,size_k,errors);
//---
   return(errors);
  }

```
