# Color

MQL5 has a special type for working with color. This allows the coloring of graphical objects.

To denote the type, the color keyword is used. For the color type value, 4 bytes of memory are allocated. Its internal representation is an unsigned integer containing a color in the RGB (Red, Green, Blue) format, that is, with separate intensity levels for red, green, and blue colors. Mixing these three components allows getting any visible color shade. Green and red will produce yellow, red and blue will do purple, etc.

1 byte is allocated for each component, that is, it can take values from 0 through 255. For instance, three zeros in all components produce a black color, while three maximum values of 255 are blended into white.

If we present color as uint in the hexadecimal notation, then the colors are distributed as follows: 0x00BBGGRR, where RR, GG, and BB are single-byte unsigned integers.

For its user's convenience, MQL5 supports a special form of literals to record color constants. Literal represents a triplet of numbers separated by commas and enclosed in single quotes. Character 'C' is placed before the literal. For instance, C'0,128,255' means a color with 0 for its red component, 128 for the green one, and 255 for the blue one. Hexadecimal notation of numbers can also be used: C'0x00,0x80,0xFF'.

Besides, a long list of predefined color shades is embedded in MQL5, all starting with clr. For example, clrMagenta, clrLightCyan, and clrYellow. They also include the primaries, of course: clrRed, clrGreen, and clrBlue. The full list can be found in the MetaEditor Help.

Below are some examples of setting colors (also available in file MQL5/Scripts/MQL5Book/p2/TypeColor.mq5):

```
void OnStart()
{
  color y = clrYellow;         // clrYellow
  color m = C'255,0,255';      // clrFuchsia
  color x = C'0x88,0x55,0x01'; // x = 136,85,1 (no such predefined color)
  color n = 0x808080;          // clrGray
}

```
