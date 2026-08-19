# PolygonAA

Draws a polygon using antialiasing algorithm.

```
void  PolygonAA(
   int&        x[],                // array of X coordinates
   int&        y[],                // array of Y coordinates
   const uint  clr,                // color
   const uint  style=UINT_MAX      // line style
   );

```

Parameters

x[]

[in]  Array of X coordinates of a polygon points.

y[]

[in]  Array of Y coordinates of a polygon points.

clr

[in]  Color in ARGB format.

style=UINT_MAX

[in]  Line style is one of [ENUM_LINE_STYLE](/en/docs/constants/indicatorconstants/drawstyles#enum_line_style) enumeration's values or a custom value.
