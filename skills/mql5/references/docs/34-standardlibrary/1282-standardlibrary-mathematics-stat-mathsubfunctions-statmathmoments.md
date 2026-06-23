# MathMoments

Calculates the first 4 moments of array elements: mean, variance, skewness, kurtosis.

```
bool  MathMoments(
   const double&  array[],            // array of values
   double&        mean,               // variable for the mean
   double&        variance,           // variable for the variance
   double&        skewness,           // variable for the skewness
   double&        kurtosis,           // variable for the kurtosis
   const int      start=0,            // initial index
   const int      count=WHOLE_ARRAY   // the number of elements
   )

```

Parameters

array[]

[in]  Array of values.

mean

[out] Variable for the mean (1st moment).

variance

[out] Variable for the variance (2nd moment).

skewness

[out] Variable for the skewness (3rd moment).

kurtosis

[out] Variable for the kurtosis (4th moment).

start=0

[in]  Initial index for calculation.

count=WHOLE_ARRAY

[in]  The number of elements for calculation.

Return Value

Returns true if the moments have been calculated successfully, otherwise false.
