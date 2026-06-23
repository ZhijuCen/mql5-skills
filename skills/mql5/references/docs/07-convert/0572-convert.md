# Conversion Functions

This is a group of functions that provide conversion of data from one format into another.

The [NormalizeDouble()](/en/docs/convert/normalizedouble) function must be specially noted as it provides the necessary accuracy of the price presentation. In trading operations, no unnormalized prices may be used if their accuracy even a digit exceeds that required by the trade server.

| Function | Action |
| --- | --- |
| CharToString | Converting a symbol code into a one-character string |
| DoubleToString | Converting a numeric value to a text line with a specified accuracy |
| EnumToString | Converting an enumeration value of any type to string |
| NormalizeDouble | Rounding of a floating point number to a specified accuracy |
| StringToDouble | Converting a string containing a symbol representation of number into number of double type |
| StringToInteger | Converting a string containing a symbol representation of number into number of long type |
| StringToTime | Converting a string containing time or date in "yyyy.mm.dd [hh:mi]" format into datetime type |
| TimeToString | Converting a value containing time in seconds elapsed since 01.01.1970 into a string of "yyyy.mm.dd hh:mi" format |
| IntegerToString | Converting int into a string of preset length |
| ShortToString | Converting symbol code (unicode) into one-symbol string |
| ShortArrayToString | Copying array part into a string |
| StringToShortArray | Symbol-wise copying a string to a selected part of array of ushort type |
| CharArrayToString | Converting symbol code (ansi) into one-symbol array |
| StringToCharArray | Symbol-wise copying a string converted from Unicode to ANSI, to a selected place of array of uchar type |
| CharArrayToStruct | Copy uchar type array to  POD structure |
| StructToCharArray | Copy  POD structure  to uchar type array |
| ColorToARGB | Converting color type to uint type to receive ARGB representation of the color. |
| ColorToPRGB | Converts the type  color  in type  uint  to get premultiplied ARGB representation of color - PRGB. |
| ColorToString | Converting color value into string as "R,G,B" |
| StringToColor | Converting "R,G,B" string or string with color name into color type value |
| StringFormat | Converting number into string according to preset format |

See also

[Use of a Codepage](/en/docs/constants/io_constants/codepageusage)
