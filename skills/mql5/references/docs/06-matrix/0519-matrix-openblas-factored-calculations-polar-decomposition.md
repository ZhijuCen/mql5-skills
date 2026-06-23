There is no special function in the OpenBLAS library to calculate the polar decomposition of a matrix. However, for this purpose can be used [singular value decomposition](/en/docs/matrix/openblas/singular_value_decomposition) (SVD):

Polar decomposition formula: A = Q * P, where:

Q - orthogonal (or unitary) matrix

P - symmetric (or Hermitian) positive-definite matrix.

How can be calculated polar decomposition using SVD.

SVD formula: A = U * Σ * VT ==> (U * VT) * (V * Σ * VT), ie Q = U * VT and P = V * Σ * VT

Example

```
//+------------------------------------------------------------------+
//| Тест функции PolarDecomposition: проверка Q ортогональна и Q*P=A |
//+------------------------------------------------------------------+
int TestPolarDecomposition(ulong size_m,ulong size_n)
  {
   matrix matrix_a=matrix::Random(size_m,size_n);
   matrix matrix_q,matrix_p;
   if(!PolarDecomposition(matrix_a,matrix_q,matrix_p))
      return(1000);
 
//--- check orthogonality
   matrix matrix_qqt=(size_m<=size_n) ? matrix_q@matrix_q.Transpose() : matrix_q.Transpose()@matrix_q;
   matrix matrix_i=matrix::Identity(matrix_qqt.Rows(),matrix_qqt.Cols());
   int    errors=(int)matrix_i.Compare(matrix_qqt,1e-11);
   printf("matrix Q is %sorthogonal",errors==0?"":"not ");
 
//--- polar decomposition test  Q * P = A
   matrix matrix_a2=matrix_q @ matrix_p;
   errors+=(int)matrix_a.Compare(matrix_a2,1e-11);
 
   printf("Polar Decomposition via SVD %s  matrix size %d x %d  errors=%d",errors==0?"passed":"failed",size_m,size_n,errors);
 
   return(errors);
  }
//+------------------------------------------------------------------+
//| Полярное разложение матрицы A = Q * P через сингулярное разлож.  |
//| Q — ортогональная, P — положит. определённая симметричная матрица|
//+------------------------------------------------------------------+
bool PolarDecomposition(matrix& matrix_a,matrix& matrix_q,matrix& matrix_p)
  {
//--- SVD
   matrix matrix_u,matrix_vt;
   vector vector_s;
   if(!matrix_a.SingularValueDecompositionDC(SVDZ_S,vector_s,matrix_u,matrix_vt))
      return(false);
 
//--- get diagonal matrix
   ulong  diag=vector_s.Size();
   matrix matrix_s=matrix::Zeros(diag,diag);
   matrix_s.Diag(vector_s);
 
//--- Q = U * VT
   matrix_q=matrix_u @ matrix_vt;
//--- P = V * Σ * VT
   matrix_p=matrix_vt.Transpose() @ matrix_s @ matrix_vt;
 
   return(true);
  }

```
