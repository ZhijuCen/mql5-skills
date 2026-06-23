# MathStandardDeviation

Calculates the standard deviation of array elements. Analog of the [sd()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/sd.html) in R.

```
double  MathStandardDeviation(
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

The standard deviation of array elements. In case of error it returns [NaN](/en/docs/basis/types/double) (not a number).
