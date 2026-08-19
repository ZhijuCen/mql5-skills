# MathProbabilityDensityWeibull

Calculates the value of the probability density function of Weibull distribution with the a and b parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityWeibull(
   const double  x,             // value of random variable
   const double  a,             // parameter of the distribution (shape)
   const double  b,             // parameter of the distribution (scale)
   const bool    log_mode,      // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability density function of Weibull distribution with the a and b parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityWeibull(
   const double  x,             // value of random variable
   const double  a,             // parameter of the distribution (shape)
   const double  b,             // parameter of the distribution (scale)
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability density function of Weibull distribution with the a and b parameters for an array of random variables x[]. In case of error it returns false. Analog of the [dweibull()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Weibull.html) in R.

```
bool  MathProbabilityDensityWeibull(
   const double& x[],            // array with the values of random variable
   const double  a,              // parameter of the distribution (shape)
   const double  b,              // parameter of the distribution (scale)
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   double&       result[]        // array for values of the probability density function
   );

```

Calculates the value of the probability density function of Weibull distribution with the a and b parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathProbabilityDensityWeibull(
   const double& x[],            // array with the values of random variable
   const double  a,              // parameter of the distribution (shape)
   const double  b,              // parameter of the distribution (scale)
   double&       result[]        // array for values of the probability density function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

a

[in]  Parameter of the distribution (scale).

b

[in]  Parameter of the distribution (shape).

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability density function.
