# LineThickHorizontal

Draws a horizontal segment of a freehand line having a specified width antialiasing.

```
void  LineThickHorizontal(
   const int      x1,            // X coordinate of the segment's first point
   const int      x2,            // X coordinate of the segment's second point
   const int      y,             // Y coordinate of the segment
   const uint     clr,           // color
   const int      size,          // line width
   const uint     style,         // line style
   ENUM_LINE_END  end_style      // line ends style
   )

```

Parameters

x1

[in]  X coordinate of the segment's first point.

x2

[in]  X coordinate of the segment's second point.

y

[in]  Segment's Y coordinate.

clr

[in]  Color in ARGB format.

size

[in]  Line width.

style

[in]  Line style is one of the ENUM_LINE_STYLE enumeration's values or a custom value.

end_style

[in]  Line style is one of the [ENUM_LINE_END](/en/docs/standardlibrary/canvasgraphics/ccanvas/ccanvaslinethick#enum_line_end) enumeration's values.
