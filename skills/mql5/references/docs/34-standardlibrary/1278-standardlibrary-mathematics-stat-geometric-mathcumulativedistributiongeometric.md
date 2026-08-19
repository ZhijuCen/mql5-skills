# MathCumulativeDistributionGeometric

Calculates the value of the probability distribution function for geometric law with the p parameter for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionGeometric(
   const double  x,             // value of random variable (integer)
   const double  p,             // parameter of the distribution (probability of event occurrence in one test)
   const bool    tail,          // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,      // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function for geometric law with the p parameter for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionGeometric(
   const double  x,             // value of random variable (integer)
   const double  p,             // parameter of the distribution (probability of event occurrence in one test)
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function for geometric law with the p parameter for an array of random variables x[]. In case of error it returns false. Analog of the [pgeom()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Geometric.html) in R.

```
bool  MathCumulativeDistributionGeometric(
   const double& x[],            // array with the values of random variable
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&       result[]        // array for values of the probability function
   );

```

Calculates the value of the probability distribution function for geometric law with the p parameter for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionGeometric(
   const double& x[],            // array with the values of random variable
   const double  p,              // parameter of the distribution (probability of event occurrence in one test)
   double&       result[]        // array for values of the probability function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

p

[in]  Parameter of the distribution (probability of event occurrence in one test).

tail

[in]  Flag of calculation, if tail=true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability function.
