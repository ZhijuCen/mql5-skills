# MathProbabilityDensityHypergeometric

Calculates the value of the probability mass function of hypergeometric distribution with the m, k and n parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityHypergeometric(
   const double  x,             // value of random variable (integer)
   const double  m,             // total number of objects (integer)
   const double  k,             // number of objects with the desired characteristic (integer)
   const double  n,             // number of object draws (integer)
   const bool    log_mode,      // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability mass function of hypergeometric distribution with the m, k and n parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityHypergeometric( 
   const double  x,             // value of random variable (integer)
   const double  m,             // total number of objects (integer)
   const double  k,             // number of objects with the desired characteristic (integer)
   const double  n,             // number of object draws (integer)
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability mass function of hypergeometric distribution with the m, k and n parameters for an array of random variables x[]. In case of error it returns false. Analog of the [dhyper()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Hypergeometric.html) in R.

```
bool  MathProbabilityDensityHypergeometric(
   const double& x[],            // array with the values of random variable
   const double  m,              // total number of objects (integer)
   const double  k,              // number of objects with the desired characteristic (integer)
   const double  n,              // number of object draws (integer)
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   double&       result[]        // array for values of the probability density function
   );

```

Calculates the value of the probability mass function of hypergeometric distribution with the m, k and n parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathProbabilityDensityHypergeometric(
   const double& x[],            // array with the values of random variable
   const double  m,              // total number of objects (integer)
   const double  k,              // number of objects with the desired characteristic (integer)
   const double  n,              // number of object draws (integer)
   double&       result[]        // array for values of the probability density function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

m

[in]  Total number of objects (integer).

k

[in]  Number of objects with the desired characteristic (integer).

n

[in]  Number of object draws (integer).

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability density function.
