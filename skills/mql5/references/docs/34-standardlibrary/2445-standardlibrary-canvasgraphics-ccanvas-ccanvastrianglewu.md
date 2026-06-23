# TriangleWu

Draws a triangle using Wu's anti-aliasing algorithm.

```
void  TriangleWu(
   const int   x1,                 // X coordinate
   const int   y1,                 // Y coordinate
   const int   x2,                 // X coordinate
   const int   y2,                 // Y coordinate
   const int   x3,                 // X coordinate
   const int   y3,                 // Y coordinate
   const uint  clr,                // color
   const uint  style=UINT_MAX      // line style
   );

```

Parameters

x1

[in]  X coordinate of the triangle's first corner.

y1

[in]  Y coordinate of the triangle's first corner.

x2

[in]  X coordinate of the triangle's second corner.

y2

[in]  Y coordinate of the triangle's second corner.

x3

[in]  X coordinate of the triangle's third corner.

y3

[in]  Y coordinate of the triangle's third corner.

clr

[in]  Color in ARGB format.

style=UINT_MAX

[in]  Line style is one of [ENUM_LINE_STYLE](/en/docs/constants/indicatorconstants/drawstyles#enum_line_style) enumeration's values or a custom value.
