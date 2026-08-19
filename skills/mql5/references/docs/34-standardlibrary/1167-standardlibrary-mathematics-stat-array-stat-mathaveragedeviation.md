# MathAverageDeviation

Calculates the average absolute deviation of array elements. Analog of the [aad()](http://artax.karlin.mff.cuni.cz/r-help/library/lsr/html/aad.html) in R.

```
double  MathAverageDeviation(
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

The average absolute deviation of array elements. In case of error it returns [NaN](/en/docs/basis/types/double) (not a number).
