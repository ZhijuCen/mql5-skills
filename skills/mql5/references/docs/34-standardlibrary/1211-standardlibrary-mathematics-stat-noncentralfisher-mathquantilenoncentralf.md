# MathQuantileF

For the specified probability, the function calculates the value of inverse noncentral Fisher's F-distribution function with the nu1, nu2 and sigma parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileF(
   const double  probability,    // probability value of random variable occurrence
   const double  nu1,            // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,            // the second parameter of distribution (number of degrees of freedom)
   const double  sigma,          // noncentrality parameter
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability, the function calculates the value of inverse noncentral Fisher's F-distribution function with the nu1, nu2 and sigma parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileF(
   const double  probability,    // probability value of random variable occurrence
   const double  nu1,            // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,            // the second parameter of distribution (number of degrees of freedom)
   const double  sigma,          // noncentrality parameter
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the value of inverse noncentral Fisher's F-distribution function with the nu1, nu2 and sigma parameters. In case of error it returns false. Analog of the [qf()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Fdist.html) in R.

```
double  MathQuantileF(
   const double& probability[],  // array with probability values of random variable
   const double  nu1,            // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,            // the second parameter of distribution (number of degrees of freedom)
   const double  sigma,          // noncentrality parameter
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   double&       result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the value of inverse noncentral Fisher's F-distribution function with the nu1, nu2 and sigma parameters. In case of error it returns false.

```
bool  MathQuantileF(
   const double& probability[],  // array with probability values of random variable
   const double  nu1,            // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,            // the second parameter of distribution (number of degrees of freedom)
   double&       result[]        // array with values of quantiles
   );

```

Parameters

probability

[in]  Probability value of random variable.

probability[]

[in]  Array with probability values of random variable.

nu1

[in]  The first parameter of distribution (number of degrees of freedom).

nu2

[in]  The second parameter of distribution (number of degrees of freedom).

sigma

[in]  Noncentrality parameter.

tail

[in]  Flag of calculation, if false, then calculation is performed for 1.0-probability.

log_mode

[in]  Flag of calculation, if log_mode=true, calculation is performed for Exp(probability).

error_code

[out]  Variable to get the error code.

result[]

[out]  Array with values of quantiles.
