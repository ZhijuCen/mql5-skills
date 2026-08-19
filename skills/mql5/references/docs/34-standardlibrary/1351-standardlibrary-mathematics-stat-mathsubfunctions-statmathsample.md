# MathSample

Generates a random sample from the array elements.

Version for working with an array of real values:

```
bool  MathSample(
   const double&  array[],           // array of values
   const int      count,             // count
   double&        result[]           // array of results
   )

```

Version for working with an array of integer values:

```
bool  MathSample(
   const int&     array[],           // array of values
   const int      count,             // count
   int&           result[]           // array of results
   )

```

Version for working with an array of real values. It is possible to obtain a sample with replacement:

```
bool  MathSample(
   const double&  array[],           // array of values
   const int      count,             // count
   const bool     replace,           // flag
   double&        result[],          // array of results
   )

```

Version for working with an array of integer values. It is possible to obtain a sample with replacement:

```
bool  MathSample(
   const int&     array[],           // array of values
   const int      count,             // count
   const bool     replace,           // flag
   int&           result[]           // array of results
   )

```

Version for working with an array of real values, for which the probabilities of sampling are defined.

```
bool  MathSample(
   const double&  array[],           // array of values
   double&        probabilities[],   // array of probabilities
   const int      count,             // count
   double&        result[]           // array of results
   )

```

Version for working with an array of integer values, for which the probabilities of sampling are defined.

```
bool  MathSample(
   const int&     array[],           // array of values
   double&        probabilities[],   // array of probabilities
   const int      count,             // count
   int&           result[]           // array of results
   )

```

Version for working with an array of real values, for which the probabilities of sampling are defined. It is possible to obtain a sample with replacement:

```
bool  MathSample(
   const double&  array[],           // array of values
   double&        probabilities[],   // array of probabilities
   const int      count,             // count
   const bool     replace,           // flag
   double&        result[]           // array of results
   )

```

Version for working with an array of integer values, for which the probabilities of sampling are defined. It is possible to obtain a sample with replacement:

```
bool  MathSample(
   const int&     array[],           // array of values
   double&        probabilities[],   // array of probabilities
   const int      count,             // count
   const bool     replace,           // flag
   int&           result[]           // array of results
   )

```

Parameters

array[]

[in] Array of integer values.

probabilities[]

[in] Array of probabilities for sampling the elements.

count

[in] The number of elements.

replace

[in]  Parameter that allows sampling with replacement.

result[]

[out] Array to output the results.

Return Value

Returns true if successful, otherwise false.

Note

The replace=true argument allows performing random sampling of the elements with replacement back to the original sequence.
