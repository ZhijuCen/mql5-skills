# MathMomentsExponential

Calculates the theoretical numerical values of the first 4 moments of the exponential distribution with the mu parameter.

```
double  MathMomentsExponential(
   const double  mu,             // parameter of the distribution (expected value)
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

mu

[in]   Parameter of the distribution (expected value).

mean

[out]  Variable to get the mean value.

variance

[out]  Variable to get the variance.

skewness

[out]  Variable to get the skewness.

kurtosis

[out]  Variable to get the kurtosis.

error_code

[out]  Variable to get the error code.

Return Value

Returns true if calculation of the moments has been successful, otherwise false.
