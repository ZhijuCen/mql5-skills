# MathTukeySummary

Calculates the Tukey's five-number summary (minimum, lower quartile, median, upper quartile, maximum) for the array elements.

```
bool  MathTukeySummary(
   const double&  array[],       // array of values
   const bool     removeNAN,     // flag
   double&        minimum,       // minimum value
   double&        lower_hinge,   // lower quartile
   double&        median,        // median value
   double&        upper_hinge,   // upper quartile
   double&        maximum        // maximum value
   )

```

Parameters

array[]

[in] Array of real values.

removeNAN

[in] Flag that indicates if non-numeric values are to be removed.

minimum

[out] Variable to store the minimum value.

lower_hinge

[out] Variable to store the lower quartile.

median

[out] Variable to store the median value.

upper_hinge

[out] Variable to store the upper quartile.

maximum

[out] Variable to store the maximum value.

Return Value

Returns true if successful, otherwise false.
