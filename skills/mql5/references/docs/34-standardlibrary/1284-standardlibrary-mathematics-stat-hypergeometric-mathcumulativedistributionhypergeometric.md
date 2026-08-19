# MathCumulativeDistributionHypergeometric

Calculates the value of the probability distribution function for hypergeometric law with the m, k and n parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionHypergeometric(
   const double  x,             // value of random variable (integer)
   const double  m,             // total number of objects (integer)
   const double  k,             // number of objects with the desired characteristic (integer)
   const double  n,             // number of object draws (integer)
   const bool    tail,          // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,      // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function for hypergeometric law with the m, k and n parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathCumulativeDistributionHypergeometric( 
   const double  x,             // value of random variable (integer)
   const double  m,             // total number of objects (integer)
   const double  k,             // number of objects with the desired characteristic (integer)
   const double  n,             // number of object draws (integer)
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability distribution function for hypergeometric law with the m, k and n parameters for an array of random variables x[]. In case of error it returns false. Analog of the [dhyper()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Hypergeometric.html) in R.

```
bool  MathCumulativeDistributionHypergeometric(
   const double& x[],            // array with the values of random variable
   const double  m,              // total number of objects (integer)
   const double  k,              // number of objects with the desired characteristic (integer)
   const double  n,              // number of object draws (integer)
   const bool    tail,           // flag of calculation, if true, then the probability of random variable not exceeding x is calculated
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated
   double&       result[]        // array for values of the distribution function
   );

```

Calculates the value of the probability distribution function for hypergeometric law with the m, k and n parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathCumulativeDistributionHypergeometric(
   const double& x[],            // array with the values of random variable
   const double  m,              // total number of objects (integer)
   const double  k,              // number of objects with the desired characteristic (integer)
   const double  n,              // number of object draws (integer)
   double&       result[]        // array for values of the distribution function
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

tail

[in]  Flag of calculation, if true, then the probability of random variable not exceeding x is calculated.

log_mode

[in]  Flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability is calculated.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the distribution function.
