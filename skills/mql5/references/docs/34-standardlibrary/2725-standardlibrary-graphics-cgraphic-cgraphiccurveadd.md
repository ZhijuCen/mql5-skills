# CurveAdd

Create and add a new curve to the chart.

This version uses the Y coordinate (a curve color is set automatically)

```
CCurve* CurveAdd(
   const double     &y[],          // Y coordinates
   ENUM_CURVE_TYPE  type,          // curve type
   const string     name=NULL      // curve name
   )

```

Note

Y array indices are used as X coordinates for the curve.

This version uses the X and Y coordinates (a curve color is set automatically)

```
CCurve*  CurveAdd(
   const double     &x[],          // X coordinates
   const double     &y[],          // Y coordinates
   ENUM_CURVE_TYPE  type,          // curve type
   const string     name=NULL      // curve name
   )

```

The version for working with CPoint2D dots (curve color is set automatically)

```
CCurve*  CurveAdd(
   const CPoint2D   &points[],     // dot coordinates
   ENUM_CURVE_TYPE  type,          // curve type
   const string     name=NULL      // curve name
   )

```

Version for working with the pointer to the CurveFunction function (curve color is set automatically)

```
CCurve*  CurveAdd(
   CurveFunction    function,      // pointer to the function
   const double     from,          // initial value of the argument
   const double     to,            // final value of the argument
   const double     step,          // increment by the argument
   ENUM_CURVE_TYPE  type,          // curve type
   const string     name=NULL      // curve name
   )

```

Version for working by Y coordinate (a curve color is set by a user)

```
CCurve*  CurveAdd(
   const double     &y[],          // Y coordinates
   const uint       clr,           // curve color
   ENUM_CURVE_TYPE  type,          // curve type
   const string     name=NULL      // curve name
   )

```

Note

Y array indices are used as X coordinates for the curve.

This version uses the X and Y coordinates (a curve color is set by a user)

```
CCurve*  CurveAdd(
   const double     &x[],          // X coordinates
   const double     &y[],          // Y coordinates
   const uint       clr,           // curve color
   ENUM_CURVE_TYPE  type,          // curve type
   const string     name=NULL      // curve name
   )

```

The version for working with CPoint2D dots (curve color is set by a user)

```
CCurve*  CurveAdd(
   const CPoint2D   &points[],     // dot coordinates
   const uint       clr,           // curve color
   ENUM_CURVE_TYPE  type,          // curve type
   const string     name=NULL      // curve name
   )

```

Version for working with the pointer to the CurveFunction function (curve color is set by a user)

```
CCurve*  CurveAdd(
   CurveFunction    function,      // pointer to the function
   const double     from,          // initial value of the argument
   const double     to,            // final value of the argument
   const double     step,          // increment by the argument
   const uint       clr,           // curve color
   ENUM_CURVE_TYPE  type,          // curve type
   const string     name=NULL      // curve name
   )

```

Parameters

&x[]

[in] X coordinate.

&y[]

[in] Y coordinate.

&points[]

[in] Coordinates of dots.

function

[in] Pointer to the function.

from

[in] Initial value of the argument.

to

[in] Final value of the argument.

step

[in] Increment by the argument.

type

[in] Curve type.

name=NULL

[in] Curve name.

clr

[in] Curve color.

Return Value

Pointer to the created curve.
