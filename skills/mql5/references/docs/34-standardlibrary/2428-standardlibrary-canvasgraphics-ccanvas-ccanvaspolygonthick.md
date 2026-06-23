# PolygonThick

Draws a polygon with a specified width using antialiasing algorithm.

```
void  PolygonThick(
   const int&      x[],          // array with the X coordinates of polygon points
   const int&      y[],          // array with the Y coordinates of polygon points
   const uint     clr,           // color
   const int      size,          // line width
   const uint     style,         // line style
   ENUM_LINE_END  end_style      // line ends style
   )

```

Parameters

x[]

[in]  Array of X coordinates of polygon points.

y[]

[in]  Array of Y coordinates of polygon points.

clr

[in]  Color in ARGB format.

size

[in]  Line width.

style

[in]  Line style is one of the ENUM_LINE_STYLE enumeration's values or a custom value.

end_style

[in]  Line style is one of the [ENUM_LINE_END](/en/docs/standardlibrary/canvasgraphics/ccanvas/ccanvaslinethick#enum_line_end) enumeration's values.
