# MathBitwiseShiftL

Calculates the result of bitwise SHL (bitwise shift left) operation for array elements.

Version with output of the results to a new array:

```
bool  MathBitwiseShiftL(
   const int&  array[],    // array of values
   const int   n,          // shift value
   int&        result[]    // array of results
   )

```

Version with output of the results to the original array:

```
bool  MathBitwiseShiftL( 
   int&        array[],    // array of values
   const int   n           // shift value
   )

```

Parameters

array[]

[in] Array of values.

n

[in] The number of bits to shift.

array[]

[out] Array of output values.

result[]

[out] Array of output values.

Return Value

Returns true if successful, otherwise false.
