# MathMomentsLognormal

Calculates the theoretical numerical values of the first 4 moments of the log-normal distribution. Returns true if calculation of the moments has been successful, otherwise false.

```
double  MathMomentsLognormal(
   const double  mu,             // logarithm of the expected value (log mean)
   const double  sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable to store the error code
   );

```

Parameters

mu

[in]  Logarithm of the expected value (log_mean).

sigma

[in]  Logarithm of the root-mean-square deviation (log standard deviation).

mean

[in]   Variable for the mean.

variance

[out]  Variable for the variance.

skewness

[out]  Variable for the skewness.

kurtosis

[out]  Variable for the kurtosis.

error code

[out]  Variable to store the error code.

Return Value

Returns true if the moments have been calculated successfully, otherwise false.
