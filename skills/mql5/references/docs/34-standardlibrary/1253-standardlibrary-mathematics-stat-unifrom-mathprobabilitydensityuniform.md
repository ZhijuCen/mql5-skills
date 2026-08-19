# MathProbabilityDensityUniform

Calculates the value of the probability density function of uniform distribution with the a and b parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityUniform(
   const double  x,             // value of random variable
   const double  a,             // distribution parameter a (lower bound)
   const double  b,             // distribution parameter b (upper bound)
   const bool    log_mode,      // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability density function of uniform distribution with the a and b parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityUniform(
   const double  x,             // value of random variable
   const double  a,             // distribution parameter a (lower bound)
   const double  b,             // distribution parameter b (upper bound)
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability density function of uniform distribution with the a and b parameters for an array of random variables x[]. In case of error it returns false. Analog of the [dunif()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Uniform.html) in R.

```
bool  MathProbabilityDensityUniform(
   const double& x[],            // array with the values of random variable
   const double  a,              // distribution parameter a (lower bound)
   const double  b,              // distribution parameter b (upper bound)
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   double&       result[]        // array for values of the probability density function
   );

```

Calculates the value of the probability density function of uniform distribution with the a and b parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathProbabilityDensityUniform(
   const double& x[],            // array with the values of random variable
   const double  a,              // distribution parameter a (lower bound)
   const double  b,              // distribution parameter b (upper bound)
   double&       result[]        // array for values of the probability density function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

a

[in]  Distribution parameter a (lower bound).

b

[in]  Distribution parameter b (upper bound).

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability density function.
