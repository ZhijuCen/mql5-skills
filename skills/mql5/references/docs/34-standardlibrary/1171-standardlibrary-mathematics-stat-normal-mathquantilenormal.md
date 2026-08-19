# MathQuantileNormal

For the specified probability, the function calculates the value of inverse normal distribution function with the mu and sigma parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileNormal(
   const double  probability,    // probability value of random variable
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   const bool    tail,           // flag for calculation of tail
   const bool    log_mode,       // calculate the logarithm of the value
   int&          error_code      // variable to store the error code
   );

```

For the specified probability, the function calculates the value of inverse normal distribution function with the mu and sigma parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileNormal(
   const double  probability,    // probability value of random variable
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the values of inverse normal distribution function with the mu and sigma parameters. In case of error it returns false. Analog of the [qnorm()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Normal.html) in R.

```
bool  MathQuantileNormal(
   const double& probability[],  // array with probability values of random variable
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   const bool    tail,           // flag for calculation of tail
   const bool    log_mode,       // calculate the logarithm of the value
   double&       result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the values of inverse normal distribution function with the mu and sigma parameters. In case of error it returns false.

```
bool  MathQuantileNormal(
   const double& probability[],  // array with probability values of random variable
   const double  mu,             // expected value
   const double  sigma,          // root-mean-square deviation
   double&       result[]        // array with values of quantiles
   );

```

Parameters

probability

[in]  Probability value of random variable.

probability[]

[in]  Array with probability values of random variable.

mu

[in]  mean parameter of the distribution (expected value).

sigma

[in]  sigma parameter of the distribution (root-mean-square deviation).

tail

[in]  Flag of calculation. If false, then calculation is performed for 1.0 - probability.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to get the error code.

result[]

[out]  Array to obtain the quantiles.
