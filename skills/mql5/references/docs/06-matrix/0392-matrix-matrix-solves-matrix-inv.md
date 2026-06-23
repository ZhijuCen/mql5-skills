# Inv

Compute the multiplicative inverse of a square invertible matrix by the Jordan-Gauss method.

```
matrix matrix::Inv()

```

Return Value

Multiplicative inverse of the matrix.

Note

The product of the original matrix and the inverse matrix is the identity matrix.

If at least one matrix row or column is zero, the inverse matrix cannot be obtained.

If two or more matrix rows or columns are linearly dependent, the inverse matrix cannot be obtained.

Example

```
int TestInverse(const int size_m)
  {
   int    i,j,errors=0;
   matrix matrix_a(size_m,size_m);
//--- populate the square matrix
   MatrixTestFirst(matrix_a);
//--- microseconds will be measured
   ulong t1=GetMicrosecondCount();
//--- get the inverse matrix
   matrix inverse=matrix_a.Inv();
//--- measure
   ulong t2=GetMicrosecondCount();
//--- check the correctness
   matrix identity=matrix_a.MatMul(inverse);
//---
   for(i=0; i<size_m; i++)
     {
      for(j=0; j<size_m; j++)
        {
         double value;
         //--- ones must be along the diagonal
         if(i==j)
            value=1.0;
         else
            value=0.0;
         if(MathClassify(identity[i][j])>FP_ZERO)
            errors++;
         else
           {
            if(identity[i][j]!=value)
              {
               double diff=MathAbs(identity[i][j]-value);
               //--- too many multiplications and devisions, so reduce the check accuracy
               if(diff>1e-9)
                  errors++;
              }
           }
        }
     }
//---
   double elapsed_time=double(t2-t1)/1000.0;
   printf("Inversion of matrix %d x %d  %s  errors=%d  time=%.3f ms",size_m,size_m,errors==0?"passed":"failed",errors,elapsed_time);
   return(errors);
  }

```
