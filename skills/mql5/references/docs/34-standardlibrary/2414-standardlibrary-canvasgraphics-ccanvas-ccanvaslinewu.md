# LineWu

Draws a segment of a freehand line using Wu's anti-aliasing algorithm.

```
void  LineWu(
   const int   x1,                 // X coordinate
   const int   y1,                 // Y coordinate
   const int   x2,                 // X coordinate
   const int   y2,                 // Y coordinate
   const uint  clr,                // color
   const uint  style=UINT_MAX      // line style
   );

```

Parameters

x1

[in]  X coordinate of the segment's first point.

y1

[in]  Y coordinate of the segment's first point.

x2

[in]  X coordinate of the segment's second point.

y2

[in]  Y coordinate of the segment's second point.

clr

[in]  Color in ARGB format.

style=UINT_MAX

[in]  Line style is one of [ENUM_LINE_STYLE](/en/docs/constants/indicatorconstants/drawstyles#enum_line_style) enumeration's values or a custom value.
