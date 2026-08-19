# MathCumulativeDistributionBinomial

Calculates the value of the probability distribution function for binomial law with the n and p parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionBinomial(
   const double  x,             // value of random variable
   const double  n,             // parameter of the distribution (number of tests)
   const double  p,             // parameter of the distribution (probability of event occurrence in one test)
   const bool    tail,          // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,      // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function for binomial law with the n and p parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionBinomial(
   const double  x,             // value of random variable
   const double  n,             // parameter of the distribution (number of tests)
   const double  p,             // parameter of the distribution (probability of event occurrence in one test)
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function for binomial law with the n and p parameters for an array of random variables x[]. In case of error it returns false. Analog of the [pweibull()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Weibull.html) in R.

```
bool  MathCumulativeDistributionBinomial(
   const double& x[],            // array with the values of random variable
   const double  n,              // parameter of the distribution (number of tests)
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&       result[]        // array for values of the probability function
   );

```

Calculates the value of the probability distribution function for binomial law with the n and p parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionBinomial(
   const double& x[],            // array with the values of random variable
   const double  n,              // parameter of the distribution (number of tests)
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   double&       result[]        // array for values of the probability function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

n

[in]  Parameter of the distribution (number of tests).

p

[in]  Parameter of the distribution (probability of event occurrence in one test).

tail

[in]  Flag of calculation. If true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability function.
