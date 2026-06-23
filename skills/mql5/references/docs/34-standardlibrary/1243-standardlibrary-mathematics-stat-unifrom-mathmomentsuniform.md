# MathMomentsUniform

Calculates the theoretical numerical values of the first 4 moments of the uniform distribution with the a and b parameters.

```
double  MathMomentsUniform(
   const double  a,              // distribution parameter a (lower bound)
   const double  b,              // distribution parameter b (upper bound)
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

a

[in]  Distribution parameter a (lower bound).

b

[in]  Distribution parameter b (upper bound).

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
