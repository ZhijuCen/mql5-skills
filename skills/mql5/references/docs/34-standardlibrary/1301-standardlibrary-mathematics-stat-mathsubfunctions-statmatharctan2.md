# MathArctan2

Returns the arctangent of the quotient of two arguments (x, y).

Version for working with the ratio of the two specified numbers (x, y):

```
double  MathArctan2(
   const double       y,         // Y coordinate
   const double       x          // X coordinate
   )

```

Return Value

Angle θ, measured in radians, so that -π≤θ≤π and tan (θ) = y or x, where (x, y) is a point in a Cartesian coordinate system.

Version for working with the ratio of the element pairs from the x and y arrays:

```
bool  MathArctan2(
   const double&      x[],       // array of x values
   const double&      y[],       // array of y values
   double&            result[]   // array of results
   )

```

Return Value

Returns true if successful, otherwise false.

Parameters

y

[in]  The Y coordinate of the point.

x

[in]  The X coordinate of the point.

x[]

[in]  Array of X coordinates of the points.

y[]

[in]  Array of Y coordinates of the points.

result[]

[out]  Array to output the results

Notes

Please note the following.

- For (x, y) in the quadrant 1, the return value will be:  0 < θ < π/2.
- For (x, y) in the quadrant 2, the return value will be:  π/2 < θ≤π.
- For (x, y) in the quadrant 3, the return value will be:  -π < θ <-π/2.
- For (x, y) in the quadrant 4, the return value will be:  -π/2 < θ < 0.

The return value for the points outside these quadrants is indicated below.

- If y is 0 and x is not negative, then θ = 0.
- If y is 0 and x is negative, then θ = π.
- If y is a positive number, and x is 0, then θ = π/2.
- If y is negative and x is 0, then θ = -π/2.
- If y is 0 and x is 0, then θ = -π/2.

If the value of the x or y parameter is NaN, or if the values of the x and y parameters are equal to the value PositiveInfinity or NegativeInfinity, the method returns the NaN value.
