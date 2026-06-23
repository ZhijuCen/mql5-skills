# TextAdd

Adds a text to a chart.

Version for working with X and Y coordinates

```
void  TextAdd(
   const int     x,               // X coordinate
   const int     y,               // Y coordinate
   const string  text,            // text
   const uint    clr,             // color
   const uint    alignment=0      // alignment
   )

```

Version for CPoint

```
void  TextAdd(
   const CPoint  &point,          // point coordinate
   const string  text,            // text
   const uint    clr,             // color
   const uint    alignment=0      // alignment
   )

```

Parameters

x

[in]  X coordinate.

y

[in]  Y coordinate.

&point

[in]  Point coordinate.

text

[in]  Text.

clr

[in]  Color.

alignment=0

[in]  Alignment.
