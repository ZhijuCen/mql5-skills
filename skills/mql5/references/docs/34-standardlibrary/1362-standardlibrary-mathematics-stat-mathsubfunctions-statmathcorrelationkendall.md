# MathCorrelationKendall

Calculates the Kendall's correlation coefficient.

Version for working with arrays of real values:

```
bool  MathCorrelationKendall(
   const double&  array1[],  // the first array of values
   const double&  array2[],  // the second array of values
   double&        tau        // correlation coefficient
   )

```

Version for working with arrays of integer values:

```
bool  MathCorrelationKendall(
   const int&     array1[],  // the first array of values
   const int&     array2[],  // the second array of values
   double&        tau        // correlation coefficient
   )

```

Parameters

array1[]

[in] The first array of values.

array2[]

[in] The second array of values.

tau

[out] Variable to store the correlation coefficient.

Return Value

Returns true if successful, otherwise false.
