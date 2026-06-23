# MathQuantileLognormal

For the specified probability, the function calculates the value of inverse log-normal distribution function with the mu and sigma parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileLognormal(
   const double  probability,    // probability value of random variable occurrence
   const double  mu,             // logarithm of the expected value (log mean)
   const double  sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability, the function calculates the value of inverse log-normal distribution function with the mu and sigma parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileLognormal(
   const double  probability,    // probability value of random variable occurrence
   const double  mu,             // logarithm of the expected value (log mean)
   const double  sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the value of inverse log-normal distribution function with the mu and sigma parameters. In case of error it returns false. Analog of the [qlnorm()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Lognormal.html) in R.

```
bool  MathQuantileLognormal(
   const double&  probability[],  // array with probability values of random variable
   const double   mu,             // logarithm of the expected value (log mean)
   const double   sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   const bool     tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool     log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   double&        result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the value of inverse log-normal distribution function with the mu and sigma parameters. In case of error it returns false.

```
bool  MathQuantileLognormal(
   const double&  probability[],  // array with probability values of random variable
   const double   mu,             // logarithm of the expected value (log mean)
   const double   sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   double&        result[]        // array with values of quantiles
   );

```

Parameters

probability

[in]  Probability value of random variable occurrence.

probability[]

[in]  Array with probability values of random variable.

mu

[in]  Logarithm of the expected value (log_mean).

sigma

[in]  Logarithm of the root-mean-square deviation (log standard deviation).

tail

[in]  Flag of calculation, if false, then calculation is performed for 1.0-probability.

log_mode

[in]  Flag of calculation, if log_mode=true, calculation is performed for Exp(probability).

error_code

[out]  Variable to store the error code.

result[]

[out]  Array with values of quantiles.
