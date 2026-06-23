# Color

The MQL5 API contains 3 built-in functions to work with the color: two of them serve for conversion of type [color](/en/book/basis/builtin_types/colors) to and from a string, and the third one provides a special color representation with transparency (ARGB).

string ColorToString(color value, bool showName = false)

The ColorToString function converts the passed color value to a string like "R,G,B" (where R, G, B are numbers from 0 to 255, corresponding to the intensity of the red, green, and blue component in the color) or to the color name from the list of predefined [web colors](https://www.mql5.com/ru/docs/constants/objectconstants/webcolors) if the showName parameter equals true. The color name is only returned if the color value exactly matches one of the webset.

Examples of using the function are given in the ConversionColor.mq5  script.

```
void OnStart()
{
   Print(ColorToString(clrBlue));            // 0,0,255
   Print(ColorToString(C'0, 0, 255', true)); // clrBlue
   Print(ColorToString(C'0, 0, 250'));       // 0,0,250
   Print(ColorToString(C'0, 0, 250', true)); // 0,0,250 (no name for this color)
   Print(ColorToString(0x34AB6821, true));   // 33,104,171 (0x21,0x68,0xAB)
}

```

color StringToColor(string text)

The StringToColor function converts a string like "R,G,B" or a string containing the name of a standard [web color](https://www.mql5.com/ru/docs/constants/objectconstants/webcolors) into a value of type [color](/en/book/basis/builtin_types/colors). If the string does not contain a properly formatted triplet of numbers or a color name, the function will return 0 (clrBlack).

Examples can be seen in the script ConversionColor.mq5.

```
void OnStart()
{
   Print(StringToColor("0,0,255")); // clrBlue
   Print(StringToColor("clrBlue")); // clrBlue
   Print(StringToColor("Blue"));    // clrBlack (no color with that name)
   // extra text will be ignored
   Print(StringToColor("255,255,255 more text"));      // clrWhite
   Print(StringToColor("This is color: 128,128,128")); // clrGray
}

```

uint ColorToARGB(color value, uchar alpha = 255)

The ColorToARGB function converts a value of type color and one-byte value alpha (specifying transparency) into an ARGB representation of a color (a value of type uint). The ARGB color format is used when creating [graphic resources](/en/book/advanced/resources/resources_resourcecreate) and [text drawing](/en/book/advanced/resources/resources_textout) on [charts](/en/book/applications/charts).

The alpha value can vary from 0 to 255. "0" corresponds to full color transparency (when displaying a pixel of this color, it leaves the existing graph image at this point unchanged), 255 means applying full color density (when displaying a pixel of this color, it completely replaces the color of the graph at the corresponding point). The value 128 (0x80) is translucent.

As we know the type color describes a color using three color components: red (Red), green (Green) and blue (Blue), which are stored in the format 0x00BBGGRR in a 4-byte integer (uint). Each component is a byte that specifies the saturation of that color in the range 0 to 255 (0x00 to 0xFF in hexadecimal). The highest byte is empty. For example, white color contains all colors and therefore has a meaning color equal to 0xFFFFFF.  

   

But in certain tasks, it is required to specify the color transparency in order to describe how the image will look when superimposed on some background (on another, already existing image). For such cases, the concept of an alpha channel is introduced, which is encoded by an additional byte.  

   

The ARGB color representation, together with the alpha channel (denoted AA), is 0xAARRGGBB. For example, the value 0x80FFFF00 means yellow (a mix of the red and green components) translucent color.

When overlaying an image with an alpha channel on some background, the resulting color is obtained:

```
Cresult = (Cforeground * alpha + Cbackground * (255 - alpha)) / 255

```

where C takes the value of each of the R, G, B components, respectively. This formula is provided for reference. When using built-in functions with ARGB colors, transparency is applied automatically.

An example of ColorToARGB application is given in ConversionColor.mq5. An auxiliary structure Argb and union ColorARGB have been added to the script for convenience when analyzing color components.

```
struct Argb
{
   uchar BB;
   uchar GG;
   uchar RR;
   uchar AA;
};
   
union ColorARGB
{
   uint value;
   uchar channels[4]; // 0 - BB, 1 - GG, 2 - RR, 3 - AA
   Argb split[1];
   ColorARGB(uint u) : value(u) { }
};

```

The structure is used as the split-type field in the union and provides access to the ARGB components by name. The union also has a byte array channels, which allows you to access components by index.

```
void OnStart()
{
   uint u = ColorToARGB(clrBlue);
   PrintFormat("ARGB1=%X", u); // ARGB1=FF0000FF
   ColorARGB clr1(u);
   ArrayPrint(clr1.split);
   /*
       [BB] [GG] [RR] [AA]
   [0]  255    0    0  255
   */
   
   u = ColorToARGB(clrDeepSkyBlue, 0x40);
   PrintFormat("ARGB2=%X", u); // ARGB2=4000BFFF
   ColorARGB clr2(u);
   ArrayPrint(clr2.split);
   /*
       [BB] [GG] [RR] [AA]
   [0]  255  191    0   64
   */
}

```

We will consider the print format function a little later, in the corresponding [section](/en/book/common/output/output_print).

There is no built-in function to convert ARGB back to color (because it is not usually required), but those who wish to do so, can use the following macro:

```
#define ARGBToColor(U) (color) \
   ((((U) & 0xFF) << 16) | ((U) & 0xFF00) | (((U) >> 16) & 0xFF))

```
