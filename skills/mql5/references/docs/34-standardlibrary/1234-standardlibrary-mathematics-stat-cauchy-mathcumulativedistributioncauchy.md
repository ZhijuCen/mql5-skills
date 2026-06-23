# MathCumulativeDistributionCauchy

Calculates the probability distribution function of Cauchy distribution with the a and b parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionCauchy(
   const double  x,             // value of random variable
   const double  a,             // mean parameter of the distribution
   const double  b,             // scale parameter of the distribution
   const bool    tail,          // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,      // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the probability distribution function of Cauchy distribution with the a and b parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionCauchy(
   const double  x,             // value of random variable
   const double  a,             // mean parameter of the distribution
   const double  b,             // scale parameter of the distribution
   int&          error_code     // variable to store the error code
   );

```

Calculates the probability distribution function of Cauchy distribution with the a and b parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionCauchy(
   const double& x[],            // array with the values of random variable
   const double  a,              // mean parameter of the distribution
   const double  b,              // scale parameter of the distribution
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&       result[]        // array for values of the probability function
   );

```

Calculates the probability distribution function of Cauchy distribution with the a and b parameters for an array of random variables x[]. In case of error it returns false. Analog of the [plogis()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Logistic.html) in R.

```
bool  MathCumulativeDistributionCauchy(
   const double& x[],            // array with the values of random variable
   const double  a,              // mean parameter of the distribution
   const double  b,              // scale parameter of the distribution
   double&       result[]        // array for values of the probability function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

a

[in]  mean parameter of the distribution.

b

[in]  scale parameter of the distribution.

tail

[in]  Flag of calculation. If true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability function.
