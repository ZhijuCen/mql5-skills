# MathProbabilityDensityExponential

Calculates the value of the probability density function of exponential distribution with the mu parameter for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityExponential(
   const double  x,             // value of random variable
   const double  mu,            // parameter of the distribution (expected value)
   const bool    log_mode,      // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability density function of exponential distribution with the mu parameter for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityExponential(
   const double  x,             // value of random variable
   const double  mu,            // parameter of the distribution (expected value)
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability density function of exponential distribution with the mu parameter for an array of random variables x[]. In case of error it returns false. Analog of the [dexp()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Exponential.html) in R.

```
bool  MathProbabilityDensityExponential(
   const double& x[],            // array with the values of random variable
   const double  mu,             // parameter of the distribution (expected value)
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   double&       result[]        // array for values of the probability density function
   );

```

Calculates the value of the probability density function of exponential distribution with the mu parameter for an array of random variables x[]. In case of error it returns false.

```
bool  MathProbabilityDensityExponential(
   const double& x[],            // array with the values of random variable
   const double  mu,             // parameter of the distribution (expected value)
   double&       result[]        // array for values of the probability density function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

mu

[in]  Parameter of the distribution (expected value)

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability density function.
