# MathKurtosis

Calculates the kurtosis (fourth moment) of array elements. Analog of the [kurtosis()](http://www.r-tutor.com/elementary-statistics/numerical-measures/kurtosis) in R (e1071 library).

```
double  MathKurtosis(
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

Kurtosis of array elements. In case of error it returns [NaN](/en/docs/basis/types/double) (not a number).

Disclaimer

Calculation of the kurtosis is performed using the excess kurtosis around the normal distribution (excess kurtosis=kurtosis-3), i.e. the excess kurtosis of a normal distribution is zero.

It is positive if the peak of the distribution around the expected value is sharp, and negative if the peak is flat.
