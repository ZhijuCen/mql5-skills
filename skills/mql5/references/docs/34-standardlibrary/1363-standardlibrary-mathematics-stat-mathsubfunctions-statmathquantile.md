# MathQuantile

Calculates sample quantiles corresponding to the specified probabilities: Q[i](p) = (1 - gamma)*x[j] + gamma*x[j+1]

```
bool  MathQuantile(
   const double&  array[],     // array of values
   const double&  probs[],     // array of probabilities
   double&        quantile[]   // array to output the quantiles
   )

```

Parameters

array[]

[in] Array of values.

probs[]

[in] Array of probabilities.

quantile[]

[out] Array to output the quantiles.

Return Value

Returns true if successful, otherwise false.
