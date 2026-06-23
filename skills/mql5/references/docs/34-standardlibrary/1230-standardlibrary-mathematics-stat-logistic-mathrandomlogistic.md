# MathRandomLogistic

Generates a pseudorandom variable distributed according to the law of logistic distribution with the mu and sigma parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathRandomLogistic(
   const double  mu,             // mean parameter of the distribution
   const double  sigma,          // scale parameter of the distribution
   int&          error_code      // variable to store the error code
   );

```

Generates pseudorandom variables distributed according to the law of logistic distribution with the mu and sigma parameters. In case of error it returns false. Analog of the [rlogis()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Logistic.html) in R.

```
bool  MathRandomLogistic(
   const double  mu,             // mean parameter of the distribution
   const double  sigma,          // scale parameter of the distribution
   const int     data_count,     // amount of required data
   double&       result[]        // array with values of pseudorandom variables
   );

```

Parameters

mu

[in]  mean parameter of the distribution.

sigma

[in]  scale parameter of the distribution.

error_code

[out]  Variable to store the error code.

data_count

[out]  Amount of required data.

result[]

[out]  Array to obtain the values of pseudorandom variables.
