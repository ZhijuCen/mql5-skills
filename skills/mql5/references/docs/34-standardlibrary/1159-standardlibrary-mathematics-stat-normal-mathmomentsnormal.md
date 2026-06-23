# MathMomentsNormal

Calculates the theoretical numerical values of the first 4 moments of the normal distribution.

```
double  MathMomentsNormal(
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable to store the error code
   );

```

Parameters

mu

[in]  mean parameter of the distribution (expected value).

sigma

[in]  sigma parameter of the distribution (root-mean-square deviation).

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

Returns true if the moments have been calculated successfully, otherwise false.
