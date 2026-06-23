# MathDifference

Generates an array with element differences of y[i]=x[i+lag]-x[i].

Version for a single generation of an array of real values:

```
bool  MathDifference(
   const double  &array[],     // array of values
   const int     lag,          // lag
   double        &result[]     // array of results
   )

```

Version for a single generation of an array of integer values:

```
bool  MathDifference(
   const int     &array[],     // array of values
   const int     lag,          // lag
   int           &result[]     // array of results
   )

```

Version for iterated generation of an array of real values (the number of iterations is set in the input parameters):

```
bool  MathDifference(
   const double  &array[],     // array of values
   const int     lag,          // lag
   const int     differences,  // number of iterations
   double        &result[]     // array of results
   )

```

Version for iterated generation of an array of integer values (the number of iterations is set in the input parameters):

```
bool  MathDifference(
   const int&    array[],      // array of values
   const int     lag,          // lag
   const int     differences,  // number of iterations
   int&          result[]      // array of results
   )

```

Parameters

array[]

[in] Array of values.

lag

[in] Lag parameter.

differences

[in] The number of iterations.

result[]

[out] Array to output the results.

Return Value

Returns true if successful, otherwise false.
