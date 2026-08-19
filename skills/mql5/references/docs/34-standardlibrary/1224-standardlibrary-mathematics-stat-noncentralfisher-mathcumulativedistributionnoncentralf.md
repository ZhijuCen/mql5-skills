# MathCumulativeDistributionNoncentralF

Calculates the value of the probability distribution function of noncentral Fisher's F-distribution with the nu1, nu2 and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionNoncentralF(
   const double  x,             // value of random variable
   const double  nu1,           // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,           // the second parameter of distribution (number of degrees of freedom)
   const double  sigma,         // noncentrality parameter
   const bool    tail,          // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,      // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function of noncentral Fisher's F-distribution with the nu1, nu2 and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionNoncentralF(
   const double  x,             // value of random variable
   const double  nu1,           // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,           // the second parameter of distribution (number of degrees of freedom)
   const double  sigma,         // noncentrality parameter
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function of noncentral Fisher's F-distribution with the nu1, nu2 and sigma parameters for an array of random variables x[]. In case of error it returns false. Analog of the [pf()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Fdist.html) in R.

```
bool  MathCumulativeDistributionNoncentralF(
   const double& x[],            // array with the values of random variable
   const double  nu1,            // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,            // the second parameter of distribution (number of degrees of freedom)
   const double  sigma,          // noncentrality parameter
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&       result[]        // array for values of the probability function
   );

```

Calculates the value of the probability distribution function of noncentral Fisher's F-distribution with the nu1, nu2 and sigma parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionNoncentralF(
   const double& x[],            // array with the values of random variable
   const double  nu1,            // the first parameter of distribution (number of degrees of freedom)
   const double  nu2,            // the second parameter of distribution (number of degrees of freedom)
   const double  sigma,          // noncentrality parameter
   double&       result[]        // array for values of the probability function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

nu1

[in]  The first parameter of distribution (number of degrees of freedom).

nu2

[in]  The second parameter of distribution (number of degrees of freedom).

sigma

[in]  Noncentrality parameter.

tail

[in]  Flag of calculation. If true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability function.
