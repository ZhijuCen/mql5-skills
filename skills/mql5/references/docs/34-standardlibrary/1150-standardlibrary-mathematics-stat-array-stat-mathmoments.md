# MathMoments

Calculates the first 4 moments (mean, variance, skewness, kurtosis) of array elements.

```
double  MathMoments(
   const double&  array[],               // array with data
   double&        mean,                  // mean (1st moment)
   double&        variance,              // variance (2nd moment)
   double&        skewness,              // skewness (3rd moment)
   double&        kurtosis,              // kurtosis (4th moment)
   const int      start=0,               // initial index 
   const int      count=WHOLE_ARRAY      // the number of elements
   );

```

Parameters

array

[in]  Array with data for calculation.

mean

[out]  Variable for the mean (1st moment)

variance

[out]  Variable for the variance (2nd moment)

skewness

[out]  Variable for the skewness (3rd moment)

kurtosis

[out]  Variable for the kurtosis (4th moment)

start=0

[in]  Initial index for calculation.

count=WHOLE_ARRAY

[in]  The number of elements for calculation.

Return Value

Returns true if the moments have been calculated successfully, otherwise false.

Disclaimer

Calculation of the kurtosis is performed using the excess kurtosis around the normal distribution (excess kurtosis=kurtosis-3), i.e. the excess kurtosis of a normal distribution is zero.

It is positive if the peak of the distribution around the expected value is sharp, and negative if the peak is flat.
