# HasNan

Return the number of [NaN](/en/docs/basis/types/double) values in a matrix/vector.

```
ulong vector::HasNan();
 
ulong matrix::HasNan();

```

Return Value

The number of matrix/vector elements that contain a NaN value.

Note

When comparing the appropriate pair of elements having NaN values, the [Compare](/en/docs/matrix/matrix_manipulations/matrix_compare) and [CompareByDigits](/en/docs/matrix/matrix_manipulations/matrix_comparebydigits) methods consider these elements equal, while in case of a usual comparison of floating-point numbers NaN != NaN.

Example:

```
void OnStart(void)
  {
   double x=sqrt(-1);
 
   Print("single: ",x==x);
 
   vector<double> v1={x};
   vector<double> v2={x};
 
   Print("vector: ", v1.Compare(v2,0)==0);
  }
 
/* Result:
 
 single: false
 vector: true
*/

```

See also

[MathClassify](/en/docs/math/mathclassify), [Compare](/en/docs/matrix/matrix_manipulations/matrix_compare), [CompareByDigits](/en/docs/matrix/matrix_manipulations/matrix_comparebydigits)
