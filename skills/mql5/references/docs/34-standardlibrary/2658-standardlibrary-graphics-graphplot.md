# GraphPlot

Functions for quick curve plotting.

Version for plotting a single curve using Y coordinates.

```
string  GraphPlot(
   const double     &y[],                  // Y coordinates
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Note

Y array indices are used as X coordinates for the curve.

Version for plotting a single curve using X and Y coordinates

```
string  GraphPlot(
   const double     &x[],                  // X coordinates
   const double     &y[],                  // Y coordinates
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Version for plotting two curves using X and Y coordinates

```
string  GraphPlot(
   const double     &x1[],                 // X coordinates
   const double     &y1[],                 // Y coordinates
   const double     &x2[],                 // X coordinates
   const double     &y2[],                 // Y coordinates
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Version for plotting three curves using X and Y coordinates

```
string  GraphPlot(
   const double     &x1[],                 // X coordinates
   const double     &y1[],                 // Y coordinates
   const double     &x2[],                 // X coordinates
   const double     &y2[],                 // Y coordinates
   const double     &x3[],                 // X coordinates
   const double     &y3[],                 // Y coordinates
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Version for plotting a curve using CPoint2D points coordinates

```
string  GraphPlot(
   const CPoint2D   &points[],             // curve coordinates
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Version for plotting two curves using CPoint2D points coordinates

```
string  GraphPlot(
   const CPoint2D   &points1[],            // curve coordinates
   const CPoint2D   &points2[],            // curve coordinates
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Version for plotting three curves using CPoint2D points coordinates

```
string  GraphPlot(
   const CPoint2D   &points1[],            // curve coordinates
   const CPoint2D   &points2[],            // curve coordinates
   const CPoint2D   &points3[],            // curve coordinates
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Version for plotting a curve using the pointer to CurveFunction

```
string  GraphPlot(
   CurveFunction    function,              // pointer to the function
   const double     from,                  // initial value of the argument
   const double     to,                    // final value of the argument
   const double     step,                  // increment by the argument
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Version for plotting two curves using the pointers to the CurveFunction functions

```
string  GraphPlot(
   CurveFunction    function1,             // pointer to the function
   CurveFunction    function2,             // pointer to the function
   const double     from,                  // initial value of the argument
   const double     to,                    // final value of the argument
   const double     step,                  // increment by the argument
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Version for plotting three curves using the pointers to the CurveFunction functions

```
string  GraphPlot(
   CurveFunction    function1,             // pointer to the function
   CurveFunction    function2,             // pointer to the function
   CurveFunction    function3,             // pointer to the function
   const double     from,                  // initial value of the argument
   const double     to,                    // final value of the argument
   const double     step,                  // increment by the argument
   ENUM_CURVE_TYPE  type=CURVE_POINTS      // curve type
   )

```

Parameters

&x[]

[in]  X coordinates.

&y[]

[in]  Y coordinates.

&x1[]

[in]  X coordinates for the first curve.

&y1[]

[in]  Y coordinates for the first curve.

&x2[]

[in]  X coordinates for the second curve.

&y2[]

[in]  Y coordinates for the second curve.

&x3[]

[in]  X coordinates for the third curve.

&y3[]

[in]  Y coordinates for the third curve.

&points[]

[in]  Coordinates of the curve dots.

&points1[]

[in]  Coordinates of the first curve dots.

&points2[]

[in]  Coordinates of the second curve dots.

&points3[]

[in]  Coordinates of the third curve dots.

function

[in] Pointer to the CurveFunction function.

function1

[in]  Pointer to the first function.

function2

[in]  Pointer to the second function.

function3

[in]  Pointer to the third function.

from

[in]  Corresponds to the first X coordinate.

to

[in]  Corresponds to the last X coordinate.

step

[in]  Parameter for calculating the X coordinates.

type=CURVE_POINTS

[in]  Curve type.

Return Value

Name of a graphical resource.
