# TextSize

Receives the text size.

```
void  TextSize(
   const string  text,       // text
   int&          width,      // width
   int&          height      // height
   );

```

Parameters

text

[in]  Text for measuring.

width

[out]  Reference to the variable for returning a text width.

height

[out]  Reference to the variable for returning a text height.

Note

The current font is used to measure the text.
