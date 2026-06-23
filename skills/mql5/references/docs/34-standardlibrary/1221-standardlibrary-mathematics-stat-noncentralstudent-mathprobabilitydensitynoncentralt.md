# MathProbabilityDensityNoncentralT

Calculates the value of the probability density function of noncentral Student's t-distribution with the nu and delta parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityNoncentralT(
   const double  x,             // value of random variable
   const double  nu,            // parameter of distribution (number of degrees of freedom)
   const double  delta,         // noncentrality parameter
   const bool    log_mode,      // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   int&          error_code     // variable for the error code
   );

```

Calculates the value of the probability density function of noncentral Student's t-distribution with the nu and delta parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityNoncentralT(
   const double  x,             // value of random variable
   const double  nu,            // parameter of distribution (number of degrees of freedom)
   const double  delta,         // noncentrality parameter
   int&          error_code     // variable for the error code
   );

```

Calculates the value of the probability density function of noncentral Student's t-distribution with the nu and delta parameters for an array of random variables x[]. In case of error it returns false. Analog of the [dt()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/TDist.html) in R.

```
bool  MathProbabilityDensityNoncentralT(
   const double& x[],            // array with the values of random variable
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   const double  delta,          // noncentrality parameter
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   double&       result[]        // array for values of the probability density function
   );

```

Calculates the value of the probability density function of noncentral Student's t-distribution with the nu and delta parameters for an array of random variables x[]. In case of error it returns false.

```
bool  MathProbabilityDensityNoncentralT(
   const double& x[],            // array with the values of random variable
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   const double  delta,          // noncentrality parameter
   double&       result[]        // array for values of the probability density function
   );

```

Parameters

x

[in]  Value of random variable.

x[]

[in]  Array with the values of random variable.

nu

[in]  Parameter of distribution (number of degrees of freedom).

delta

[in]  Noncentrality parameter.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability density function.
