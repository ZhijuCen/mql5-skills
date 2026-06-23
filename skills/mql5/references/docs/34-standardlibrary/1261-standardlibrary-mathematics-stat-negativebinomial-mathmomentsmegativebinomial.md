# MathMomentsNegativeBinomial

Calculates the theoretical numerical values of the first 4 moments of the negative binomial distribution with the r and p parameters.

```
double  MathMomentsNegativeBinomial(
   const double  r,              // number of successful tests
   const double  p,              // probability of success
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

r

[in]  Number of successful tests.

p

[in]  Probability of success.

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
