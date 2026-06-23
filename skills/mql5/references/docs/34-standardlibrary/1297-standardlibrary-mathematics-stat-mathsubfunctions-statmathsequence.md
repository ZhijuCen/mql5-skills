# MathSequence

Generates a sequence of values based on the following values: the first element, the last element, the step of the sequence.

Version for working with real values:

```
bool  MathSequence(
   const double  from,       // initial value
   const double  to,         // final value
   const double  step,       // step
   double&       result[]    // array of results
   )

```

Version for working with integer values:

```
bool  MathSequence(
   const int     from,       // initial value
   const int     to,         // final value
   const int     step,       // step
   int&          result[]    // array of results
   )

```

Parameters

from

[in] The first value of the sequence

to

[in] The last value of the sequence

step

[in] The step of the sequence.

result[]

[out] Array to output the sequence.

Return Value

Returns true if successful, otherwise false.
