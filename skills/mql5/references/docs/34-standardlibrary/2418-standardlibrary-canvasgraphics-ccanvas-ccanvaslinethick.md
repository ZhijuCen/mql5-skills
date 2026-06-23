# LineThick

Draws a segment of a freehand line having a specified width using antialiasing algorithm.

```
void  LineThick(
   const int      x1,            // X coordinate of the segment's first point 
   const int      y1,            // Y coordinate of the segment's first point
   const int      x2,            // X coordinate of the segment's second point
   const int      y2,            // Y coordinate of the segment's second point
   const uint     clr,           // color 
   const int      size,          // line width
   const uint     style,         // line style
   ENUM_LINE_END  end_style      // line ends style
   )

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

size

[in]  Line width.

style

[in]  Line style is one of the ENUM_LINE_STYLE enumeration's values or a custom value.

end_style

[in]  Line style is one of the ENUM_LINE_END enumeration's values

ENUM_LINE_END

| ID | Description |
| --- | --- |
| LINE_END_ROUND | Line ends are rounded. |
| LINE_END_BUTT | Line ends are cut. |
| LINE_END_SQUARE | A line ends in a filled rectangle. |
