# MathRandomT

Generates a pseudorandom variable distributed according to the law of Student's t-distribution with the nu parameter. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathRandomT(
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   int&          error_code      // variable to store the error code
   );

```

Generates pseudorandom variables distributed according to the law of Student's t-distribution with the nu parameter. In case of error it returns false. Analog of the [rt()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/TDist.html) in R.

```
bool  MathRandomT(
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   const int     data_count,     // amount of required data
   double&       result[]        // array with values of pseudorandom variables
   );

```

Parameters

nu

[in] Parameter of distribution (number of degrees of freedom).

error_code

[out]  Variable to store the error code.

data_count

[out]  Amount of required data.

result[]

[out]  Array to obtain the values of pseudorandom variables.
