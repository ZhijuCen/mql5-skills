# MathQuantileChiSquare

For the specified probability, the function calculates the value of inverse chi-squared distribution function. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileChiSquare(
   const double  probability,    // probability value of random variable occurrence
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability, the function calculates the value of inverse chi-squared distribution function. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileChiSquare(
   const double  probability,    // probability value of random variable occurrence
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the value of inverse chi-squared distribution function. In case of error it returns false. Analog of the [qchisq()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Chisquare.html) in R.

```
double  MathQuantileChiSquare(
   const double& probability[],  // array with probability values of random variable
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   double&       result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the value of inverse chi-squared distribution function. In case of error it returns false.

```
bool  MathQuantileChiSquare(
   const double& probability[],  // array with probability values of random variable
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   double&       result[]        // array with values of quantiles
   );

```

Parameters

probability

[in]  Probability value of random variable.

probability[]

[in]  Array with probability values of random variable.

nu

[in]  Parameter of distribution (number of degrees of freedom).

tail

[in]  Flag of calculation, if false, then calculation is performed for 1.0-probability.

log_mode

[in]  Flag of calculation, if log_mode=true, calculation is performed for Exp(probability).

error_code

[out]  Variable to get the error code.

result[]

[out]  Array with values of quantiles.
