# PolylineThick

Draws a polyline with a specified width using antialiasing algorithm.

```
void  PolylineThick(
   const int      &x[],          // array with the X coordinates of polyline points
   const int      &y[],          // array with the Y coordinates of polyline points
   const uint     clr,           // color
   const int      size,          // line width
   const uint     style,         // line style
   ENUM_LINE_END  end_style      // line ends style
   )

```

Parameters

&x[]

[in]  Array of X coordinates of a polyline.

&y[]

[in]  Array of Y coordinates of a polyline.

clr

[in]  Color in ARGB format.

size

[in]  Line width.

style

[in]  Line style is one of the ENUM_LINE_STYLE enumeration's values or a custom value.

end_style

[in]  Line style is one of the [ENUM_LINE_END](/en/docs/standardlibrary/canvasgraphics/ccanvas/ccanvaslinethick#enum_line_end) enumeration's values
