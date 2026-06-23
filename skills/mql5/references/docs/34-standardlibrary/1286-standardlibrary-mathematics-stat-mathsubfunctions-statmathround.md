# MathRound

Rounds a double-precision floating-point number or an array of such numbers to the specified number of decimal places.

Version for rounding a double-precision floating-point number to the specified number of decimal places:

```
double  MathRound(
   const double   x,          // value of the number
   const int      digits      // the number of decimal places
   )

```

Return Value

A number nearest to the x parameter, with the number of decimal places equal to digits.

Version for rounding an array of double-precision floating-point numbers to the specified number of decimal places. The results are output to a new array.

```
bool  MathRound(
   const double&  array[],    // array of values
   int            digits,     // the number of decimal places
   double&        result[]    // array of results
   )

```

Return Value

Returns true if successful, otherwise false.

Version for rounding an array of double-precision floating-point numbers to the specified number of decimal places. The results are output to the original array.

```
bool  MathRound(
   double&        array[],    // array of values
   int            digits      // the number of decimal places
   )

```

Return Value

Returns true if successful, otherwise false.

Parameters

x

[in]  Double-precision floating-point number to be rounded.

digits

[in]  The number of decimal places in the returned value.

array[]

[in]  Array of double-precision floating-point numbers to be rounded.

array[]

[out]  Array of output values.

result[]

[out]  Array of output values.
