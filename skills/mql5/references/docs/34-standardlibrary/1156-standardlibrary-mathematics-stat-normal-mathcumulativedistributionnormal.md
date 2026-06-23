# MathCumulativeDistributionNormal

Calculates the value of the normal distribution function with the mu and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionNormal(
   const double  x,              // value of random variable
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   const bool    tail,           // flag for calculation of tail
   const bool    log_mode,       // calculate the logarithm of the value
   int&          error_code      // variable to store the error code
   );

```

Calculates the value of the normal distribution function with the mu and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionNormal(
   const double  x,              // value of random variable
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   int&          error_code      // variable to store the error code
   );

```

Calculates the value of the normal distribution function with the mu and sigma parameters for an array of random variables x[]. In case of error it returns false. Analog of the [dnorm()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Normal.html) in R.

```
bool  MathCumulativeDistributionNormal(
   const double& x[],            // array with the values of random variable
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   const bool    tail,           // flag for calculation of tail
   const bool    log_mode,       // calculate the logarithm of the value
   double&       result[]        // array for values of the probability function
   );

```

Calculates the value of the normal distribution function with the mu and sigma parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionNormal(
   const double& x[],            // array with the values of random variable
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   double&       result[]        // array for values of the probability function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

mu

[in]  mean parameter of the distribution (expected value).

sigma

[in]  sigma parameter of the distribution (root-mean-square deviation).

tail

[in]  Flag of calculation. If tail=true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to get the error code.

result[]

[out]  Array to obtain the values of the probability function.
