# MaxGrace (Get method)

Returns the "tolerance" applied to the axis maximum.

```
double  MaxGrace()

```

Return Value

"Tolerance" value for the axis maximum.

Note

This value is expressed as part of the overall axial length. For example, suppose that the axis values are located within 4.0 to 16.0, then its length is 12.0. If MaxGrace is equal to 0.1, then 10% of the axis length (or 1.2) is added to the maximum value. As a result, the axis covers the interval from 4.0 to 17.2.

# MaxGrace (Set method)

Sets the "tolerance" applied to the axis maximum.

```
void  MaxGrace(
   const double  value      // "tolerance" value
   )

```

Parameters

value

[in] "Tolerance" value applied to the axis maximum.

Note

This value is expressed as part of the overall axial length. For example, suppose that the axis values are located within 4.0 to 16.0, then its length is 12.0. If MinGrace is equal to 0.1, then 10% of the axis length (or 1.2) is subtracted from the minimum value. As a result, the axis covers the interval from 2.8 to 16.0.
