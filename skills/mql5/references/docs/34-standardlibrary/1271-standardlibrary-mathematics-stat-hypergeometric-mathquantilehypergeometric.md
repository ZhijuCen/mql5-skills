# MathQuantileHypergeometric

For the specified probability, the function calculates the inverse value of distribution function for hypergeometric law with the m, k and n parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileHypergeometric(
   const double  probability,    // probability value of random variable occurrence
   const double  m,              // total number of objects (integer)
   const double  k,              // number of objects with the desired characteristic (integer)
   const double  n,              // number of object draws (integer)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability, the function calculates the inverse value of distribution function for hypergeometric law with the m, k and n parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileHypergeometric(
   const double  probability,    // probability value of random variable occurrence
   const double  m,              // total number of objects (integer)
   const double  k,              // number of objects with the desired characteristic (integer)
   const double  n,              // number of object draws (integer)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the inverse value of distribution function for hypergeometric law with the m, k and n parameters. In case of error it returns false. Analog of the [qhyper()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Hypergeometric.html) in R.

```
double  MathQuantileHypergeometric(
   const double& probability[],  // array with probability values of random variable
   const double  m,              // total number of objects (integer)
   const double  k,              // number of objects with the desired characteristic (integer)
   const double  n,              // number of object draws (integer)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   double&       result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the inverse value of distribution function for hypergeometric law with the m, k and n parameters. In case of error it returns false.

```
bool  MathQuantileHypergeometric(
   const double& probability[],  // array with probability values of random variable
   const double  m,              // total number of objects (integer)
   const double  k,              // number of objects with the desired characteristic (integer)
   const double  n,              // number of object draws (integer)
   double&       result[]        // array with values of quantiles
   );

```

Parameters

probability

[in]  Probability value of random variable.

probability[]

[in]  Array with probability values of random variable.

m

[in]  Total number of objects (integer).

k

[in]  Number of objects with the desired characteristic (integer).

n

[in]  Number of object draws (integer).

tail

[in]  Flag of calculation, if tail=false, then calculation is performed for 1.0-probability.

log_mode

[in]  Flag of calculation, if log_mode=true, calculation is performed for Exp(probability).

error_code

[out]  Variable to get the error code.

result[]

[out]  Array with values of quantiles.
