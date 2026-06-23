# CompareByDigits

Compare the elements of two matrices/vectors with the significant digits precision.

```
ulong vector::CompareByDigits(
  const vector& vec,          // vector to compare
  const int     digits        // number of significant digits
   );
 
ulong matrix::CompareByDigits(
  const matrix& mat,          // matrix to compare
  const int     digits        // number of significant digits
   );

```

Parameters

vec

[in]  Vector to compare.

mat

[in]  Matrix to compare.

digits

[in] Number of significant digits to compare.

Return Value

The number of mismatched elements of the matrices or vectors being compared: 0 if the matrices are equal, greater than 0 otherwise.

Note

The comparison operators == or != execute an exact element-wise comparison. It is known that the exact comparison of real numbers is of limited use, so the epsilon comparison method was added. It may happen that one matrix can contain elements in a range, for example from 1e-20 to 1e+20. Such matrices can be processed using element-wise comparison up to significant digits.

Example

```
   int    size_m=128;
   int    size_k=256;
   matrix matrix_a(size_m,size_k);
//--- fill the matrix
   double  value=0.0;
   for(int i=0; i<size_m; i++)
     {
      for(int j=0; j<size_k; j++)
        {
         if(i==j)
            matrix_a[i][j]=1.0+i;
         else
           {
            value+=1.0;
            matrix_a[i][j]=value/1e+20;
           }
        }
     }
//--- get another matrix
   matrix matrix_c = matrix_a * -1;
 
   ulong errors_epsilon=matrix_a.Compare(matrix_c,1e-15);
   ulong errors_digits=matrix_a.CompareByDigits(matrix_c,15);
 
   printf("Compare matrix %d x %d  errors_epsilon=%I64u  errors_digits=%I64u",size_m,size_k,errors_epsilon,errors_digits);
 
 
  /*
  Compare matrix 128 x 256  errors_epsilon=128  errors_digits=32768
  */

```
