# MathTrunc

Calculates the integer part of the specified number or array elements.

Version for working with a double-precision floating-point number:

```
double  MathTrunc(
   const double   x          // value of the number
   )

```

Return Value

The integer part of the specified number.

Version for working with an array of double-precision floating-point numbers. The results are output to a new array:

```
bool  MathTrunc(
   const double&  array[],   // array of values
   double&        result[]   // array of results
   )

```

Return Value

Returns true if successful, otherwise false.

Version for working with an array of double-precision floating-point numbers. The results are output to the original array:

```
bool  MathTrunc(
   double&        array[]    // array of values
   )

```

Return Value

Returns true if successful, otherwise false.

Parameters

x

[in]  Double-precision floating-point number, the integer part of which is to be obtained.

array[]

[in] Array of double-precision floating-point numbers, the integer parts of which are to be obtained.

array[]

[out] Array of output values.

result[]

[out] Array of output values.
