# LineAdd

Adds a line to a chart.

This version uses X and Y coordinates

```
void  LineAdd(
   const int   x1,        // x1 coordinate
   const int   y1,        // y1 coordinate
   const int   x2,        // x2 coordinate
   const int   y2,        // y2 coordinate
   const uint  clr,       // color
   const uint  style      // style
   )

```

Version for CPoint

```
void  LineAdd2(
   const CPoint  &point1,     // first point coordinate
   const CPoint  &point2,     // second point coordinate
   const uint    clr,         // color
   const uint    style        // style
   )

```

Parameters

x1

[in]  X1 coordinate.

y1

[in]  Y1 coordinate.

x2

[in]  X2 coordinate.

y2

[in]  Y2 coordinate.

&point1

[in]  First point coordinate.

&point2

[in]  Second point coordinate.

clr

[in]  Color.

style

[in]  Style.
