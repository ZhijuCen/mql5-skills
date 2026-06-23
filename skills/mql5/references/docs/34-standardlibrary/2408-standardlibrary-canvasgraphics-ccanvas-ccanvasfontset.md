# FontSet

Sets the current font.

```
bool  FontSet(
   const string  name,        // name
   const int     size,        // size
   const uint    flags=0,     // flags
   const uint    angle=0      // angle
   );

```

Parameters

name

[in]  Font name. For example, "Arial".

size

[in]  Font size. See [TextSetFont()](/en/docs/objects/textsetfont) function description to learn more about setting a size.

flags=0

[in]  Font creation flags. See [TextSetFont()](/en/docs/objects/textsetfont) function description to learn more about the flags.

angle=0

[in]  Font slope angle in tenths of a degree.

Return Value

true - successful, otherwise - false
