# MathMomentsPoisson

Calculates the theoretical numerical values of the first 4 moments of the Poisson distribution with the lambda parameter.

```
double  MathMomentsPoisson(
   const double  lambda,         // parameter of the distribution (mean)
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

lambda

[in]  Parameter of the distribution (mean).

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
