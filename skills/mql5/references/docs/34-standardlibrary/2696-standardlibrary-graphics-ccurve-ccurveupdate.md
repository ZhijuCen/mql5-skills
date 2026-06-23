# Update

Update the curve coordinates.

The version for working by Y coordinate. Passed array indexes are used as X coordinates here.

```
void  Update(
   const double&  y[]   // Y coordinates    
   )

```

This version uses X and Y coordinates.

```
void  Update(
   const double&  x[],     // X coordinates  
   const double&  y[]      // Y coordinates    
   )

```

The version for working with CPoint2D points.

```
void  Update(
   const CPoint2D&  points[]      // Curve coordinates
   )

```

The version for working with a pointer to the CurveFunction function.

```
void  Update(
   CurveFunction  function,     // pointer to the function describing a curve
   const double   from,         // initial value of the function argument
   const double   to,           // final value of the function argument
   const double   step          // argument increment
   )

```

Parameters

x[]

[in]  X coordinates.

y[]

[in]  Y coordinates.

points[]

[in]  Curve coordinates.

function

[in] A pointer to the function describing a curve

from

[in]  Initial value of the function argument

to

[in]  End value of the function argument

step

[in]  Argument increment
