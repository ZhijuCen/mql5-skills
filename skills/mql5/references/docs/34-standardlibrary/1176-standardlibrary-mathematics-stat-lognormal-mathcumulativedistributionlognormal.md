# MathCumulativeDistributionLognormal

Calculates the log-normal distribution function of probabilities with the mu and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionLognormal(
   const double  x,              // value of random variable
   const double  mu,             // logarithm of the expected value (log mean)
   const double  sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is returned
   int&          error_code      // variable to store the error code
   );

```

Calculates the log-normal distribution function of probabilities with the mu and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionLognormal(
   const double  x,              // value of random variable
   const double  mu,             // logarithm of the expected value (log mean)
   const double  sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   int&          error_code      // variable to store the error code
   );

```

Calculates the log-normal distribution function of probabilities with the mu and sigma parameters for an array of random variables x[]. In case of error it returns false. Analog of the [plnorm()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Lognormal.html) in R.

```
bool  MathCumulativeDistributionLognormal(
   const double&  x[],            // array with the values of random variable
   const double   mu,             // logarithm of the expected value (log mean)
   const double   sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   const bool     tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool     log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&        result[]        // array for values of the probability function
   );

```

Calculates the log-normal distribution function of probabilities with the mu and sigma parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionLognormal(
   const double&  x[],            // array with the values of random variable
   const double   mu,             // logarithm of the expected value (log mean)
   const double   sigma,          // logarithm of the root-mean-square deviation (log standard deviation)
   double&        result[]        // array for values of the probability function
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

tail

[in]  Flag of calculation, if true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array to obtain the values of the probability function.
