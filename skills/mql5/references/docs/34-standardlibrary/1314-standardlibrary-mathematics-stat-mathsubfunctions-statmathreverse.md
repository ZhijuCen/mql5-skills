# MathReverse

Generates an array of values with reverse order of elements.

Version for working with real values and with output of the results to a new array:

```
bool  MathReverse(
   const double&  array[],      // array of values
   double&        result[]      // array of results
   )

```

# Version for working with integer values and with output of the results to a new array:

```
bool  MathReverse(
   const int&     array[],      // array of values
   int&           result[]      // array of results
   )

```

# Version for working with real values and with output of the results to the original array.

```
bool  MathReverse(
   double&        array[]       // array of values
   )

```

# Version for working with integer values and with output of the results to the original array:

```
bool  MathReverse(
   int&           array[]       // array of values
   )

```

Parameters

array[]

[in] Array of values.

array[]

[out] Output array with the reverse order of values.

result[]

[out] Output array with the reverse order of values.

Return Value

Returns true if successful, otherwise false.
