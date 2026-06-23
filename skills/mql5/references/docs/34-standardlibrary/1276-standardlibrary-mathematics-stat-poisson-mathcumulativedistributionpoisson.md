# MathCumulativeDistributionPoisson

Calculates the value of the Poisson distribution function with the lambda parameter for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionPoisson(
   const double  x,             // value of random variable (integer)
   const double  lambda,        // parameter of the distribution (mean)
   const bool    tail,          // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,      // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the Poisson distribution function with the lambda parameter for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionPoisson( 
   const double  x,             // value of random variable (integer)
   const double  lambda,        // parameter of the distribution (mean)
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the Poisson distribution function with the lambda parameter for an array of random variables x[]. In case of error it returns false. Analog of the [dhyper()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Hypergeometric.html) in R.

```
bool  MathCumulativeDistributionPoisson(
   const double& x[],            // array with the values of random variable
   const double  lambda,         // parameter of the distribution (mean)
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&       result[]        // array for values of the distribution function
   );

```

Calculates the value of the Poisson distribution function with the lambda parameter for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionPoisson(
   const double& x[],            // array with the values of random variable
   const double  lambda,         // parameter of the distribution (mean)
   double&       result[]        // array for values of the distribution function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

lambda

[in]  Parameter of the distribution (mean).

tail

[in]  Flag of calculation, if true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the distribution function.
