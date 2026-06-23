# MathQuantileNoncentralBeta

Calculates the value of the inverse probability distribution function of noncentral beta distribution with the a, b and lambda parameters for the occurrence probability of a random variable probability. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileNoncentralBeta(
   const double  probability,    // probability value of random variable occurrence
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const double  lambda,         // noncentrality parameter
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   int&          error_code      // variable to store the error code
   );

```

Calculates the value of the inverse probability distribution function of noncentral beta distribution with the a, b and lambda parameters for the occurrence probability of a random variable probability. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileNoncentralBeta(
   const double  probability,    // probability value of random variable occurrence
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const double  lambda,         // noncentrality parameter
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the value of the inverse probability distribution function of noncentral beta distribution with the a, b and lambda parameters. In case of error it returns false. Analog of the [qbeta()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Beta.html) in R.

```
double  MathQuantileNoncentralBeta(
   const double&  probability[],  // array with probability values of random variable
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const double  lambda,         // noncentrality parameter
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   double&       result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the value of the inverse probability distribution function of noncentral beta distribution with the a, b and lambda parameters. In case of error it returns false.

```
bool  MathQuantileNoncentralBeta(
   const double& probability[],  // array with probability values of random variable
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const double  lambda,         // noncentrality parameter
   double&       result[]        // array with values of quantiles
   );

```

Parameters

probability

[in]  Probability value of random variable.

probability[]

[in]  Array with probability values of random variable.

a

[in]  The first parameter of beta distribution (shape1).

b

[in]  The second parameter of beta distribution (shape2).

lambda

[in]   Noncentrality parameter.

tail

[in]   Flag of calculation, if false, then calculation is performed for 1.0-probability.

log_mode

[in]   Flag of calculation, if log_mode=true, calculation is performed for Exp(probability).

error_code

[out]  Variable to get the error code.

result[]

[out]  Array with values of quantiles.
