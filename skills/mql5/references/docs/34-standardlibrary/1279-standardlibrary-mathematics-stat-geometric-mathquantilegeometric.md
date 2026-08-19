# MathQuantileGeometric

For the specified probability, the function calculates the inverse value of distribution function for geometric law with the p parameter. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileGeometric(
   const double  probability,    // probability value of random variable occurrence
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability, the function calculates the inverse value of distribution function for geometric law with the p parameter. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileGeometric(
   const double  probability,    // probability value of random variable occurrence
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the inverse value of distribution function for geometric law with the p parameter. In case of error it returns false. Analog of the [qgeom()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Geometric.html) in R.

```
double  MathQuantileGeometric(
   const double& probability[],  // array with probability values of random variable
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   double&       result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the inverse value of distribution function for geometric law with the p parameter. In case of error it returns false.

```
bool  MathQuantileGeometric(
   const double& probability[],  // array with probability values of random variable
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   double&       result[]        // array with values of quantiles
   );

```

Parameters

probability

[in]  Probability value of random variable.

probability[]

[in]  Array with probability values of random variable.

p

[in]  Parameter of the distribution (probability of event occurrence in one test).

tail

[in]  Flag of calculation, if false, then calculation is performed for 1.0-probability.

log_mode

[in]  Flag of calculation, if log_mode=true, calculation is performed for Exp(probability).

error_code

[out]  Variable to get the error code.

result[]

[out]  Array with values of quantiles.
