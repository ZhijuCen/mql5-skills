# MathQuantileBeta

For the specified probability, the function calculates the value of inverse beta distribution function with the a and b parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileBeta(
   const double  probability,    // probability value of random variable occurrence
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability, the function calculates the value of inverse beta distribution function with the a and b parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathQuantileBeta(
   const double  probability,    // probability value of random variable occurrence
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   int&          error_code      // variable to store the error code
   );

```

For the specified probability[] array of probability values, the function calculates the values of inverse beta distribution function with the a and b parameters. In case of error it returns false. Analog of the [qbeta()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Beta.html) in R.

```
double  MathQuantileBeta(
   const double&  probability[], // array with probability values of random variable
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const bool    tail,           // flag of calculation, if false, then calculation is performed for 1.0-probability
   const bool    log_mode,       // flag of calculation, if log_mode=true, calculation is performed for Exp(probability)
   double&       result[]        // array with values of quantiles
   );

```

For the specified probability[] array of probability values, the function calculates the values of inverse beta distribution function with the a and b parameters. In case of error it returns false.

```
bool  MathQuantileBeta(
   const double& probability[],  // array with probability values of random variable
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
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

tail

[in]  Flag of calculation, if lower_tail=false, then calculation is performed for 1.0-probability.

log_mode

[in]  Flag of calculation, if log_mode=true, calculation is performed for Exp(probability).

error_code

[out]  Variable to get the error code.

result[]

[out]  Array with values of quantiles.
