# MathMomentsNoncentralBeta

Calculates the theoretical numerical values of the first 4 moments of the noncentral beta distribution with the a, b and lambda parameters.

```
double  MathMomentsNoncentralBeta(
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const double  lambda,         // noncentrality parameter
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

a

[in]   The first parameter of beta distribution (shape1).

b

[in]   The second parameter of beta distribution (shape2).

lambda

[in]   Noncentrality parameter

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
