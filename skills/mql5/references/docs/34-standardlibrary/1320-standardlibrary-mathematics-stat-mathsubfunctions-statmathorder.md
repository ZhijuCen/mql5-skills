# MathOrder

Generates an integer array with permutation according to order of the array elements after sorting.

Version for working with an array of real values:

```
bool  MathOrder(
   const double&  array[],   // array of values
   int&           result[]   // array of results
   )

```

Version for working with an array of integer values:

```
bool  MathOrder(
   const int&     array[],   // array of values
   int&           result[]   // array of results
   )

```

Parameters

array[]

[in] Array of values.

result[]

[out] Array to output the sorted indexes.

Return Value

Returns true if successful, otherwise false.
