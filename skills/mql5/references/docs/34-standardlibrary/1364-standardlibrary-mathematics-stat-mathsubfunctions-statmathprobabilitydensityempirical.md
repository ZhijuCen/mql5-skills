# MathProbabilityDensityEmpirical

The function calculates the empirical probability density function (pdf) for random values from an array.

```
bool  MathProbabilityDensityEmpirical(
   const double&  array[],   // array of random values
   const int      count,     // the number of pairs
   double&        x[],       // array of x values
   double&        pdf[]      // array of pdf values
   )

```

Parameters

array[]

[in] Array of random values.

count

[in] The number of (x, pdf(x)) pairs.

x[]

[out] Array to output the x values.

pdf[]

[out] Array to output the pdf(x) values.

Return Value

Returns true if successful, otherwise false.
