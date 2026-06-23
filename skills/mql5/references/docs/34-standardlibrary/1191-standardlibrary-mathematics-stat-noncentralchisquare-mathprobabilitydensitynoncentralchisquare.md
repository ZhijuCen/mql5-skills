# MathProbabilityDensityNoncentralChiSquare

Calculates the value of the probability density function of noncentral chi-squared distribution with the nu and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityNoncentralChiSquare(
   const double  x,             // value of random variable
   const double  nu,            // parameter of distribution (number of degrees of freedom)
   const double  sigma,         // noncentrality parameter
   const bool    log_mode,      // calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability density function of noncentral chi-squared distribution with the nu and sigma parameters for a random variable x. In case of error it returns [NaN](/en/docs/basis/types/double).

```
double  MathProbabilityDensityNoncentralChiSquare(
   const double  x,             // value of random variable
   const double  nu,            // parameter of distribution (number of degrees of freedom)
   const double  sigma,         // noncentrality parameter
   int&          error_code     // variable to store the error code
   );

```

Calculates the value of the probability density function of noncentral chi-squared distribution with the nu and sigma parameters for an array of random variables x[]. In case of error it returns false. Analog of the [dchisq()](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Chisquare.html) in R.

```
bool  MathProbabilityDensityNoncentralChiSquare(
   const double& x[],            // array with the values of random variable
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   const double  sigma,          // noncentrality parameter
   const bool    log_mode,       // flag to calculate the logarithm of the value, if log_mode=true, then the natural logarithm of the probability density is calculated
   double&       result[]        // array for values of the probability density function
   );

```

Calculates the value of the probability density function of noncentral chi-squared distribution with the nu parameter for an array of random variables x[]. In case of error it returns false.

```
bool  MathProbabilityDensityNoncentralChiSquare(
   const double& x[],            // array with the values of random variable
   const double  nu,             // parameter of distribution (number of degrees of freedom)
   const double  sigma,          // noncentrality parameter
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

sigma

[in]  Noncentrality parameter.

log_mode

[in]  Flag to calculate the logarithm of the value. If log_mode=true, then the natural logarithm of the probability density is returned.

error_code

[out]  Variable to store the error code.

result[]

[out]  Array for values of the probability density function.
