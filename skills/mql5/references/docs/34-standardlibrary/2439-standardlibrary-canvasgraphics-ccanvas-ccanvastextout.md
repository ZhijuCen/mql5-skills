# TextOut

Displays text.

```
void  TextOut(
   int         x,               // X coordinate
   int         y,               // Y coordinate
   string      text,            // text
   const uint  clr,             // color
   uint        alignment=0      // alignment
   );

```

Parameters

x

[in]  Text anchor's X coordinate.

y

[in]  Text anchor's Y coordinate.

text

[in]  Text to be displayed.

clr

[in]  Color in ARGB format.

alignment=0

[in]  Text anchoring method. See [TextOut()](/en/docs/objects/textout) function description to learn more about anchoring methods.

Note

The current font is used to display the text.
