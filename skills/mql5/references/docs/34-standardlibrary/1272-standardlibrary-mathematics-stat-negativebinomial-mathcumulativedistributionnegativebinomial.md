# MathCumulativeDistributionNegativeBinomial

Calculates the value of the probability distribution function for negative binomial law with the r and p parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionNegativeBinomial(
   const double  x,             // value of random variable (integer)
   const double  r,             // number of successful tests
   const double  p,             // probability of success
   const bool    tail,          // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,      // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function for negative binomial law with the r and p parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionNegativeBinomial(
   const double  x,             // value of random variable (integer)
   const double  r,             // number of successful tests
   const double  p,             // probability of success
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function for negative binomial law with the r and p parameters for an array of random variables x[]. In case of error it returns false. Analog of the [pweibull()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Weibull.html) in R.

```
bool  MathCumulativeDistributionNegativeBinomial(
   const double& x[],            // array with the values of random variable
   const double  r,              // number of successful tests
   const double  p,              // probability of success
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&       result[]        // array for values of the probability function
   );

```

Calculates the value of the probability distribution function for negative binomial law with the r and p parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionNegativeBinomial(
   const double& x[],            // array with the values of random variable
   const double  r,              // number of successful tests
   const double  p,              // probability of success
   double&       result[]        // array for values of the probability function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

r

[in]  Number of successful tests.

p

[in]  Probability of success.

tail

[in]  Flag of calculation, if true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability function.
