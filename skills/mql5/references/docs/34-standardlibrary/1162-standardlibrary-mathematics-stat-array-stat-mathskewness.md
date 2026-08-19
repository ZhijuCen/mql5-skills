# MathSkewness

Calculates the skewness (third moment) of array elements. Analog of the [skewness()](http://www.r-tutor.com/elementary-statistics/numerical-measures/skewness) in R (e1071 library).

```
double  MathSkewness(
   const double&  array[]                // array with data
   );

```

Parameters

array

[in]  Array with data for calculation.

start=0

[in]  Initial index for calculation.

count=WHOLE_ARRAY

[in]  The number of elements for calculation.

Return Value

Skewness of array elements. In case of error it returns [NaN](/en/docs/basis/types/double) (not a number).
