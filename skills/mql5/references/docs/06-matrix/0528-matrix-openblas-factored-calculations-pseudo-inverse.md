There is no special function in the OpenBLAS library to calculate the pseudo-inverse of a matrix. However, for this purpose can be used [singular value decomposition](/en/docs/matrix/openblas/singular_value_decomposition) (SVD):

1. Decompose matrix A into U * Σ * VT

2. Invert Σ (non-zero singular values ​​only)

3. Get the pseudo-inverse matrix using the formula

A+ = V * Σ+ * UT

Example

```
//+------------------------------------------------------------------+
//|  Тест функции PseudoInverse: проверка A * A+ * A ≈ A             |
//+------------------------------------------------------------------+
int TestPseudoInverse(ulong size_m,ulong size_n)
  {
   matrix matrix_a=matrix::Random(size_m,size_n);
   matrix matrix_pi;
   if(!PseudoInverse(matrix_a,matrix_pi))
      return(1000);
 
//--- pseudo inverse test  A * A+ * A = A
   matrix matrix_a2=matrix_a @ matrix_pi @ matrix_a;
   int    errors=(int)matrix_a.Compare(matrix_a2,1e-11);
 
   printf("Pseudo Inverse via SVD %s  matrix size %d x %d  errors=%d",errors==0?"passed":"failed",size_m,size_n,errors);
 
   return(errors);
  }
//+------------------------------------------------------------------+
//| Вычисляет псевдообратную матрицу с помощью сингулярного разлож.  |
//| A+ = V * Σ⁻¹ * Uᵀ                                                |
//+------------------------------------------------------------------+
bool PseudoInverse(matrix& matrix_a,matrix& matrix_pi)
  {
//--- 1. SVD
   matrix matrix_u,matrix_vt;
   vector vector_s;
   if(!matrix_a.SingularValueDecompositionDC(SVDZ_S,vector_s,matrix_u,matrix_vt))
      return(false);
 
//--- 2. inverse diagonal matrix
   ulong  diag=vector_s.Size();
   matrix matrix_si=matrix::Zeros(diag,diag);
   for(ulong i=0; i<diag; i++)
     {
      if(vector_s[i]!=0.0)
         matrix_si[i][i]=1.0/vector_s[i];
     }
 
//--- 3. pseudo inverse  A+ = V * Σ+ * UT
   matrix_pi=matrix_vt.Transpose() @ matrix_si @ matrix_u.Transpose();
 
   return(true);
  }

```
