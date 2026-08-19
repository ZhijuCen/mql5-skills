# MathSignif

Rounds a value to the specified number of digits in the mantissa.

Version for working with a real value:

```
double  MathSignif(
   const double   x,         // value
   const int      digits     // number of decimal places
   )

```

Return Value

The rounded value.

Version for working with an array of real values and with output of the results to a separate array:

```
bool  MathSignif(
   const double&  array[],   // array of values
   int            digits,    // number of decimal places
   double         result[]   // array of results
   )

```

Return Value

Returns true if successful, otherwise false.

Version for working with an array of real values and with output of the results to the original array:

```
bool  MathSignif(
   double&        array[],   // array of values
   int            digits     // number of decimal places
   )

```

Return Value

Returns true if successful, otherwise false.

Parameters

x

[in] Real value to be rounded.

digits

[in] Number of decimal places.

array[]

[in] Array of real values.

array[]

[out] Array of output values.

result[]

[out] Array of output values.
