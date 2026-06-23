# MathMomentsLogistic

Calculates the theoretical numerical values of the first 4 moments of the logistic distribution with the mu and sigma parameters.

```
double  MathMomentsLogistic(
   const double  mu,             // mean parameter of the distribution
   const double  sigma,          // scale parameter of the distribution
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

mu

[in]  mean parameter of the distribution.

sigma

[in]  scale parameter of the distribution.

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
