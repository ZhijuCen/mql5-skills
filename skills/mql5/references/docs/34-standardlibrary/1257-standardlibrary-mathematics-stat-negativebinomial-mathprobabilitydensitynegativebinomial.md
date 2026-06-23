# MathProbabilityDensityNegativeBinomial

Calculates the value of the probability mass function of negative binomial distribution with the r and p parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityNegativeBinomial(
   const double  x,             // value of random variable (integer)
   const double  r,             // number of successful tests
   const double  p,             // probability of success
   const bool    log_mode,      // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability mass function of negative binomial distribution with the r and p parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityNegativeBinomial( 
   const double  x,             // value of random variable (integer)
   const double  r,             // number of successful tests
   const double  p,             // probability of success
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability mass function of negative binomial distribution with the r and p parameters for an array of random variables x[]. In case of error it returns false. Analog of the [dnbinom()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/NegBinomial.html) in R.

```
bool  MathProbabilityDensityNegativeBinomial(
   const double& x[],            // array with the values of random variable
   const double  r,              // number of successful tests
   const double  p,              // probability of success
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   double&       result[]        // array for values of the probability density function
   );

```

Calculates the value of the probability mass function of negative binomial distribution with the r and p parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathProbabilityDensityNegativeBinomial(
   const double& x[],            // array with the values of random variable
   const double  r,              // number of successful tests
   const double  p,              // probability of success
   double&       result[]        // array for values of the probability density function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

r

[in]  Number of successful tests

p

[in]  Probability of success.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability density function.
