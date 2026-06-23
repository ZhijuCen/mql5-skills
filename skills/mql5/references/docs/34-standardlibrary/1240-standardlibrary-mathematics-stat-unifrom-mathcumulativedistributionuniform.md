# MathCumulativeDistributionUniform

Calculates the probability distribution function of uniform distribution with the a and b parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionUniform(
   const double  x,             // value of random variable
   const double  a,             // distribution parameter a (lower bound)
   const double  b,             // distribution parameter b (upper bound)
   const bool    tail,          // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,      // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the probability distribution function of uniform distribution with the a and b parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionUniform(
   const double  x,             // value of random variable
   const double  a,             // distribution parameter a (lower bound)
   const double  b,             // distribution parameter b (upper bound)
   int&          error_code     // variable to store the error code
   );

```

Calculates the probability distribution function of uniform distribution with the a and b parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionUniform(
   const double& x[],            // array with the values of random variable
   const double  a,              // distribution parameter a (lower bound)
   const double  b,              // distribution parameter b (upper bound)
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&       result[]        // array for values of the probability function
   );

```

Calculates the probability distribution function of uniform distribution with the a and b parameters for an array of random variables x[]. In case of error it returns false. Analog of the [punif()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Uniform.html) in R.

```
bool  MathCumulativeDistributionUniform(
   const double& x[],            // array with the values of random variable
   const double  a,              // distribution parameter a (lower bound)
   const double  b,              // distribution parameter b (upper bound)
   double&       result[]        // array for values of the probability function
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

tail

[in]  Flag of calculation. If true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability function.
