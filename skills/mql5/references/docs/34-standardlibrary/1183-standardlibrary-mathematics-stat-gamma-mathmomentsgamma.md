# MathMomentsGamma

Calculates the theoretical numerical values of the first 4 moments of the gamma distribution with the a and b parameters.

```
double  MathMomentsGamma(
   const double  a,              // the first parameter of the distribution (shape)
   const double  b,              // the second parameter of the distribution (scale)
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

a

[in]   The first parameter of the distribution (shape).

b

[in]   The second parameter of the distribution (scale).

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
