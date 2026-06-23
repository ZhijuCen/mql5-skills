# MathQuantilePoisson

For the specified probability, the function calculates the inverse value of Poisson distribution function with the lambda parameter. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantilePoisson(
   const double  probability,    // probability value of random variable occurrence
   const double  lambda,         // parameter of the distribution (mean)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability, the function calculates the inverse value of Poisson distribution function with the lambda parameter. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantilePoisson(
   const double  probability,    // probability value of random variable occurrence
   const double  lambda,         // parameter of the distribution (mean)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the inverse value of Poisson distribution function with the lambda parameter. In case of error it returns false. Analog of the [qhyper()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Hypergeometric.html) in R.

```
double  MathQuantilePoisson(
   const double& probability[],  // array with probability values of random variable
   const double  lambda,         // parameter of the distribution (mean)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   double&       result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the inverse value of Poisson distribution function with the lambda parameter. In case of error it returns false.

```
bool  MathQuantilePoisson(
   const double& probability[],  // array with probability values of random variable
   const double  lambda,         // parameter of the distribution (mean)
   double&       result[]        // array with values of quantiles
   );

```

Parameters

probability

[in]  Probability value of random variable.

probability[]

[in]  Array with probability values of random variable.

lambda

[in]  Parameter of the distribution (mean).

tail

[in]  Flag of calculation, if tail=false, then calculation is performed for 1.0-probability.

log_mode

[in]  Flag of calculation, if log_mode=true, calculation is performed for Exp(probability).

error_code

[out]  Variable to get the error code.

result[]

[out]  Array with values of quantiles.
