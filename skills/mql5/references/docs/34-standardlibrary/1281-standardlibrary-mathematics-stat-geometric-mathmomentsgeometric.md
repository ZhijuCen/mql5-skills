# MathMomentsGeometric

Calculates the theoretical numerical values of the first 4 moments of the geometric distribution with the p parameter.

```
double  MathMomentsGeometric(
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

p

[in]  Parameter of the distribution (probability of event occurrence in one test).

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
