# MathMomentsNoncentralF

Calculates the theoretical numerical values of the first 4 moments of the noncentral Fisher's F-distribution with the nu1, nu2 and sigma parameters.

```
double  MathMomentsNoncentralF(
   const double  nu1,            // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,            // the second parameter of distribution (number of degrees of freedom)
   const double  sigma,          // noncentrality parameter
   double&       mean,           // variable for the mean
   double&       variance,       // variable for the variance  
   double&       skewness,       // variable for the skewness
   double&       kurtosis,       // variable for the kurtosis
   int&          error_code      // variable for the error code
   );

```

Parameters

nu1

[in]  The first parameter of distribution (number of degrees of freedom).

nu2

[in]  The second parameter of distribution (number of degrees of freedom).

sigma

[in]  Noncentrality parameter.

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
