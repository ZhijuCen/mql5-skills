# MathReplicate

Generates a repeating sequence of values.

Version for working with real values:

```
bool  MathReplicate(
   const double&  array[],    // array of values
   const int      count,      // number of repetitions
   double&        result[]    // array of results
   )

```

Version for working with integer values:

```
bool  MathReplicate(
   const int&     array[],    // array of values
   const int      count,      // number of repetitions
   int&           result[]    // array of results
   )

```

Parameters

array[]

[in] Array for generating a sequence.

count

[in] The number of the array repetitions in the sequence.

result[]

[out] Array to output the sequence.

Return Value

Returns true if successful, otherwise false.
