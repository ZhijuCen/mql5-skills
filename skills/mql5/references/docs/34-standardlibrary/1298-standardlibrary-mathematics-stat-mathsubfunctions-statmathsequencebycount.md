# MathSequenceByCount

Generates a sequence of values based on the following values: the first element, the last element, the number of elements in the sequence.

Version for working with real values:

```
bool  MathSequenceByCount(
   const double  from,       // initial value
   const double  to,         // final value
   const int     count,      // count
   double&       result[]    // array of results
   )

```

Version for working with integer values:

```
bool  MathSequenceByCount(
   const int     from,       // initial value
   const int     to,         // final value
   const int     count,      // count
   int&          result[]    // array of results
   )

```

Parameters

from

[in] The first value of the sequence.

to

[in] The last value of the sequence.

count

[in] The number of elements in the sequence.

result[]

[out] Array to output the sequence.

Return Value

Returns true if successful, otherwise false.
