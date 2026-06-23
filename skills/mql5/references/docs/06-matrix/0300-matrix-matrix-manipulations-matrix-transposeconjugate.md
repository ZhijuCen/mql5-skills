# TransposeConjugate

Transposing a complex matrix with conjugation. Reverse or permute the axes of a matrix by changing a sign of an imaginary part of a complex number, return the modified matrix.

```
matrixc matrixc::TransposeConjugate()

```

Return Value

Transposed complex conjugate matrix.

Note

Conjugate can be applied to real (non-complex) matrix or vector. In this case matrix or vector just copied on return.

Simple algorithm of transposing a complex matrix with conjugation - method explanation

```
//--- Complex matrix transpose function with conjugation
matrixc MatrixTransposeConjugate(const matrixc& matrix_a)
  {
   //--- create a new matrix_c with dimensions inverse to matrix_a
   matrixc matrix_c(matrix_a.Cols(), matrix_a.Rows());
 
   //--- go through all the rows of the new matrix
   for(ulong i=0; i<matrix_c.Rows(); i++)
     {
      //--- go through all the columns of the new matrix
      for(ulong j=0; j<matrix_c.Cols(); j++)
        {
         //--- transfer the real part of the element by transposing the index
         matrix_c[i][j].real = matrix_a[j][i].real;
         //--- transfer the imaginary part of the element by changing the sign (conjugation)
         matrix_c[i][j].imag = -matrix_a[j][i].imag;
        }
     }
 
    //--- return the transposed matrix with conjugation
    return(matrix_c);
  }

```
