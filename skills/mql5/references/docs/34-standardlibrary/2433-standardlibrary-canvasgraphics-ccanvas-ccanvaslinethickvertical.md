# LineThickVertical

Draws a vertical segment of a freehand line having a specified width using antialiasing algorithm.

```
void  LineThickVertical(
   const int      x,             // X coordinate of the segment
   const int      y1,            // Y coordinate of the segment's first point
   const int      y2,            // Y coordinate of the segment's second point
   const uint     clr,           // color
   const int      size,          // line width
   const uint     style,         // line style
   ENUM_LINE_END  end_style      // line ends style
   )

```

Parameters

x

[in]  Segment's X coordinate.

y1

[in]  Y coordinate of the segment's first point.

y2

[in]  Y coordinate of the segment's second point.

clr

[in]  Color in ARGB format.

size

[in]  Line width.

style

[in]  Line style is one of the ENUM_LINE_STYLE enumeration's values or a custom value.

end_style

[in]  Line style is one of the [ENUM_LINE_END](/en/docs/standardlibrary/canvasgraphics/ccanvas/ccanvaslinethick#enum_line_end) enumeration's values.
