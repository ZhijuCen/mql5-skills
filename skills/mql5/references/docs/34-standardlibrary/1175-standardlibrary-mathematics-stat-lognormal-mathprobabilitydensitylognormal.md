# MathProbabilityDensityLognormal

Calculates the value of the probability density function of log-normal distribution with the mu and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityLognormal(
   const double  x,              // value of random variable
   const double  mu,             // logarithm of the expected value (log mean)
   const double  sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   const bool    log_mode,       // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   int&          error_code      // variable to store the error code
   );

```

Calculates the value of the probability density function of log-normal distribution with the mu and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityLognormal(
   const double  x,              // value of random variable
   const double  mu,             // logarithm of the expected value (log mean)
   const double  sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   int&          error_code      // variable to store the error code
   );

```

Calculates the value of the probability density function of log-normal distribution with the mu and sigma parameters for an array of random variables x[]. In case of error it returns [NaN](/en/docs/basis/types/double). Analog of the [dlnorm()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Lognormal.html) in R.

```
bool  MathProbabilityDensityLognormal(
   const double&  x[],            // array with the values of random variable
   const double   mu,             // logarithm of the expected value (log mean)
   const double   sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   const bool     log_mode,       // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   double&        result[]        // array for values of the probability density function
   );

```

Calculates the value of the probability density function of log-normal distribution with the mu and sigma parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathProbabilityDensityLognormal(
   const double&  x[],            // array with the values of random variable
   const double   mu,             // logarithm of the expected value (log mean)
   const double   sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   double&        result[]        // array for values of the probability density function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

mu

[in]  Logarithm of the expected value (log_mean).

sigma

[in]  Logarithm of the root-mean-square deviation (log standard deviation).

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array to obtain the values of the probability density function.
