# MathRandomUniform

Generates a pseudorandom variable distributed according to the law of uniform distribution with the a and b parameters. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathRandomUniform(
   const double  a,              // distribution parameter a (lower bound)
   const double  b,              // distribution parameter b (upper bound)
   int&          error_code      // variable to store the error code
   );

```

Generates pseudorandom variables distributed according to the law of uniform distribution with the a and b parameters. In case of error it returns false. Analog of the [runif()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Uniform.html) in R.

```
bool  MathRandomUniform(
   const double  a,              // distribution parameter a (lower bound)
   const double  b,              // distribution parameter b (upper bound)
   const int     data_count,     // amount of required data
   double&       result[]        // array with values of pseudorandom variables
   );

```

Parameters

a

[in]  Distribution parameter a (lower bound).

b

[in]  Distribution parameter b (upper bound).

error_code

[out]  Variable to store the error code.

data_count

[out]  Amount of required data.

result[]

[out]  Array to obtain the values of pseudorandom variables.
