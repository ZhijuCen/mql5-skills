# MathRandomBeta

Generates a pseudorandom variable distributed according to the law of beta distribution with the a and b parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathRandomBeta(
   const double  a,             // the first parameter of beta distribution (shape1)
   const double  b,             // the second parameter of beta distribution (shape2)
   int&          error_code     // variable to store the error code
   );

```

Generates pseudorandom variables distributed according to the law of beta distribution with the a and b parameters. In case of error it returns false. Analog of the [rbeta()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Beta.html) in R.

```
bool  MathRandomBeta(
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const int     data_count,     // amount of required data
   double&       result[]        // array to obtain the pseudorandom variables
   );

```

Parameters

a

[in]  The first parameter of beta distribution (shape1)

b

[in]  The second parameter of beta distribution (shape2).

data_count

[in]  The number of pseudorandom variables to be obtained.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array to obtain the values of pseudorandom variables.
