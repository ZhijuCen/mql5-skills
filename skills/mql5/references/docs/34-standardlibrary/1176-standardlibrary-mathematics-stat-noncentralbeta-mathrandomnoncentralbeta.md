# MathRandomNoncentralBeta

Generates a pseudorandom variable distributed according to the law of noncentral beta distribution the a, b and lambda parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathRandomNoncentralBeta(
   const double  a,             // the first parameter of beta distribution (shape1)
   const double  b,             // the second parameter of beta distribution (shape2)
   const double  lambda,        // noncentrality parameter
   int&          error_code     // variable to store the error code
   );

```

Generates pseudorandom variables distributed according to the law of noncentral beta distribution the a, b and lambda parameters. In case of error it returns false. Analog of the [rbeta()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Beta.html) in R.

```
bool  MathRandomNoncentralBeta(
   const double  a,              // the first parameter of beta distribution (shape1)
   const double  b,              // the second parameter of beta distribution (shape2)
   const double  lambda,         // noncentrality parameter
   const int     data_count,     // amount of required data
   double&       result[]        // array to obtain the pseudorandom variables
   );

```

Parameters

a

[in]  The first parameter of beta distribution (shape1)

b

[in]  The second parameter of beta distribution (shape2).

lambda

[in]  Noncentrality parameter

error_code

[out]  Variable to store the error code.

data_count

[out]  Amount of required data.

result[]

[out]  Array to obtain the values of pseudorandom variables.
