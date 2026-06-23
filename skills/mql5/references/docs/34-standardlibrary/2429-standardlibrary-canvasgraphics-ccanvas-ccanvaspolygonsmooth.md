# PolygonSmooth

Draws a polygon with a specified width consecutively using two antialiasing algorithms First, individual segments are smoothed based on Bezier curves. Then, the raster antialiasing algorithm is applied to the polygon built from these segments to improve the rendering quality.

```
void  PolygonSmooth(
   int&             x[],                          // array with the X coordinates of polygon points
   int&             y[],                          // array with the Y coordinates of polygon points
   const uint       clr,                          // color
   const int        size,                         // line width
   ENUM_LINE_STYLE  style=STYLE_SOLID,            // line style
   ENUM_LINE_END    end_style=LINE_END_ROUND,     // line ends style
   double           tension=0.5,                  // antialiasing parameter value
   double           step=10                       // length of approximation lines
   )

```

Parameters

&x[]

[in]  Array of X coordinates of polygon points.

&y[]

[in]  Array of Y coordinates of polygon points.

clr

[in]  Color in ARGB format.

size

[in]  Line width.

style=STYLE_SOLID

[in]  Line style is one of the ENUM_LINE_STYLE enumeration's values or a custom value.

end_style=LINE_END_ROUND

[in]  Line style is one of the [ENUM_LINE_END](/en/docs/standardlibrary/canvasgraphics/ccanvas/ccanvaslinethick#enum_line_end) enumeration's values.

tension=0.5

[in]  Smoothing parameter value.

step=10

[in]  Length of approximating lines.
