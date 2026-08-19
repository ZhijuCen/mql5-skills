# ColorToPRGB

Converts the type [color](/en/docs/basis/types/integer/color) in type [uint](/en/docs/basis/types/integer/integertypes#uint) to get premultiplied ARGB representation of color - PRGB. PRGB color format is used when creating [graphic resource](/en/docs/runtime/resources), [text output](/en/docs/objects/textout) and in the CCanvas standard library class with the color format [COLOR_FORMAT_ARGB_RAW](/en/docs/common/resourcecreate#enum_color_format)  (components are not processed by the terminal and must be correctly prepared by the user).

```
uint  ColorToPRGB(
   color  clr,          // converted color in color format
   uchar  alpha=255     // alpha channel that controls color transparency
   );

```

Parameters

clr

[in] Value of color in a variable of type color.

alpha

[in] Value of alpha channel, to get color in format [ARGB](/en/docs/common/resourcecreate). It is set from 0 (the color of the superimposed pixel does not change the display of the underlying pixel at all) to 255 (the color is superimposed completely and overlaps the color of the underlying pixel). Color transparency in percentage terms is calculated as (1-alpha/255)*100%, i.e. the lower the alpha channel value, the more transparent the color is.

Return value

Color representation in ARGB format, where four bytes of uint type contain the values Alfa, Red, Green, Blue (alpha channel, red, green, blue).

Note

How does PRGB differ from ARGB?

There are two common representations of RGBA color with an alpha channel:

- straight (normal) ARGB - RGB is stored "as is", alpha is separate;
- premultiplied (PRGB) - RGB is already multiplied by alpha.

Mode [COLOR_FORMAT_ARGB_RAW](/en/docs/common/resourcecreate#enum_color_format) assumes that color components are already correctly prepared and the terminal does not "normalize/recalculate" them. Therefore, in scenarios where premultiplied-color is expected, it is PRGB that should be passed, otherwise visual artifacts/mismatches during rendering may occur.

PRGB color is calculated by the formula:

R = R * A / 255

G = G * A / 255

B = B * A / 255

A = A

Special Cases:

- when alpha = 255 the result coincides with ColorToARGB(clr,255) (multiplication does not change RGB);
- when alpha = 0 the result becomes 0x00000000 (fully transparent pixel, RGB = 0).

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
{
   uchar alpha = 0x55; // 0x55 = 85; transparency ~ (255-85)/255 * 100% = 66.7%
   color c = clrWhite;
 
   PrintFormat("0x%%.8X - %s", c, ColorToString(c,true));
   PrintFormat("0x%.8X - ARGB (straight)", ColorToARGB(c, alpha));
   PrintFormat("0x%.8X - PRGB (premultiplied)", ColorToPRGB(c, alpha));
   /*
   0x00FFFFFF - clrWhite
   0x55FFFFFF - ARGB (straight)
   0x55555555 - PRGB (premultiplied)
   */
}

```

See also

[Resources](/en/docs/runtime/resources), [ColorToARGB](/en/docs/convert/colortoargb), [ResourceCreate()](/en/docs/common/resourcecreate), [TextOut()](/en/docs/objects/textout), [Color type](/en/docs/basis/types/integer/color), [Types char, short, int and long](/en/docs/basis/types/integer/integertypes)
