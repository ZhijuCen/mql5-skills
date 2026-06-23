# ColorToString

It converts color value into string of "R,G,B" form.

```
string  ColorToString(
   color  color_value,     // color value
   bool   color_name       // show color name or not
   );

```

Parameters

color_value

[in]  Color value in color type variable.

color_name

[in]  Return color name if it is identical to one of predefined [color constants](/en/docs/constants/objectconstants/webcolors).

Return Value

String presentation of color as "R,G,B", where R, G and B are decimal constants from 0 to 255 converted into a string. If the color_name=true parameter is set, it will try to convert color value into color name.

Example:

```
   string clr=ColorToString(C'0,255,0'); // green color
   Print(clr);
 
   clr=ColorToString(C'0,255,0',true);   // get color constant
   Print(clr);

```

See also

[StringToColor](/en/docs/convert/stringtocolor), [ColorToARGB](/en/docs/convert/colortoargb)
