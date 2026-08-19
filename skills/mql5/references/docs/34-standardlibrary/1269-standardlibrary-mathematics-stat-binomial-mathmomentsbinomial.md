# MathMomentsBinomial

Calculates the theoretical numerical values of the first 4 moments of the binomial distribution with the n and p parameters.

```
double  MathMomentsBinomial(
   const double  n,              // parameter of the distribution (number of tests)
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

n

[in]  Parameter of the distribution (number of tests).

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
