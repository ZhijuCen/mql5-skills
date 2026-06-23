# PrintFormat

It formats and enters sets of symbols and values in the Expert Advisor log in accordance with a preset format.

```
void  PrintFormat(
   string format_string,   // format string
   ...                     // values of simple types
   );

```

Parameters

format_string

[in]  A format string consists of simple symbols, and if the format string is followed by arguments, it also contains format specifications.

...

[in]  Any values of simple types separated by commas. Total number of parameters can't exceed 64 including the format string.

Return Value

String.

Note

PrintFormat() function does not work during optimization in the [Strategy Tester](/en/docs/runtime/testing#print).

The number, order and type of parameters must exactly match the set of qualifiers, otherwise the print result is undefined. Instead of PrintFormat() you can use printf().

If the format string is followed by parameters, this string must contain format specifications that denote output format of these parameters. Specification of format always starts with the percent sign (%).

A format string is read from left to right. When the first format specification is met (if there is any), the value of the first parameter after the format string is transformed and output according to the preset specification. The second format specification calls transformation and output of the second parameter, and so on till the format string end.

The format specification has the following form:

%[flags][width][.precision][{h | l | ll | I32 | I64}]type

Each field of the format specification is either a simple symbol, or a number denoting a simple format option. The simplest format specification contains only the percent sign (%) and a symbol defining the [type of the output parameter](/en/docs/common/printformat#type) (for example, %s). If you need to output the percent sign in the format string, use the format specification %%.

## flags

| Flag | Description | Default Behavior |
| --- | --- | --- |
| – (minus) | Left justification within the set width | Right justification |
| + (plus) | Output of the + or - sign for values of sign types | The sign is shown only if the value is negative |
| 0 (zero) | Zeroes are added before an output value within the preset  width . If  0  flag is specified with an integer format ( i ,  u ,  x ,  X ,  o ,  d ) and accuracy specification is set (for example, %04.d), then 0 is ignored. | Nothing is added |
| space | A space is shown before an output value, if it is a sign and positive value | Spaces aren't inserted |
| # | If used together with the format  o ,  x  or  X , then before the output value 0, 0x or 0X is added respectively. | Nothing is added |
|  | If used together with the format  e ,  E ,  a  or  A , value is always shown with a decimal point. | Decimal point is shown only if there is a non-zero fractional part. |
|  | If used together with the format  g  or  G , flag defines presence of a decimal point in the output value and prevents the cutting off of leading zeroes.  
 Flag # is ignored when used together with formats  c ,  d ,  i ,  u ,  s . | Decimal point is shown only if there is a non-zero fractional part. Leading zeroes are cut off. |

## width  #

A non-negative decimal number that sets the minimal number of output symbols of the formatted value. If the number of output symbols is less than the specified width, the corresponding number of spaces is added from the left or right depending on the alignment (flag –). If there is flag zero (0), the corresponding number of zeroes is added before the output value. If the number of output symbols is greater than the specified width, the output value is never cut off.

If an asterisk (*) is specified as width, value of int type must be indicated in the corresponding place of the list of passed parameters. It will be used for specifying width of the output value.

## precision  #

A non-negative decimal number that sets the output precision - number of digits after a decimal point. As distinct from width specification, precision specification can cut off the part of fractional type with or without rounding.

The use of precision specification is different for different format [types](/en/docs/common/printformat#type).

| Types | Description | Default Behavior |
| --- | --- | --- |
| a, A | Precision specification sets the number of digits after a decimal point. | Default precision – 6. |
| c, C | Not used |  |
| d, i, u, o, x, X | Sets minimal number of output digits. If number of digits in a corresponding parameter is less than this precision, zeroes are added to the left of the output value. The output value isn't cut off, if the number of output digits is larger than the specified precision. | Default precision – 1. |
| e, E, f | Sets number of output digits after a decimal point. The last digit is rounded off. | Default precision – 6. If set precision is 0 or decimal part is absent, the decimal point is not shown. |
| g, G | Sets maximal number of meaningful numbers. | 6 meaningful numbers are output. |
| s | Sets number of output symbols of a string. If the string length exceeds the precision, the string is cut off. | The whole string is output. |

```
   PrintFormat("1. %s", _Symbol);
   PrintFormat("2. %.3s", _Symbol);
   int length=4;
   PrintFormat("3. %.*s", length, _Symbol);
   /*
   1. EURUSD
   2. EUR
   3. EURU
   /

```

## h | l | ll | I32 | I64

Specification of data sizes, passed as a parameter.

| Parameter Type | Used Prefix | Joint Specifier of Type |
| --- | --- | --- |
| int | l (lower case L) | d, i, o, x, or X |
| uint | l (lower case L) | o, u, x, or X |
| long | ll (two lower case L) | d, i, o, x, or X |
| short | h | d, i, o, x, or X |
| ushort | h | o, u, x, or X |
| int | I32 | d, i, o, x, or X |
| uint | I32 | o, u, x, or X |
| long | I64 | d, i, o, x, or X |
| ulong | I64 | o, u, x, or X |

## type  #

Type specifier is the only obligatory field for formatted output.

| Symbol | Type | Output Format |
| --- | --- | --- |
| c | int | Symbol of short type (Unicode) |
| C | int | Symbol of char type (ANSI) |
| d | int | Signed decimal integer |
| i | int | Signed decimal integer |
| o | int | Unsigned octal integer |
| u | int | Unsigned decimal integer |
| x | int | Unsigned hexadecimal integer, using "abcdef" |
| X | int | Unsigned hexadecimal integer, using "ABCDEF" |
| e | double | A real value in the format [-] d.dddde[sign] ddd, where d - one decimal digit, dddd - one or more decimal digits, ddd - a three-digit number that determines the size of the exponent, sign - plus or minus |
| E | double | Similar to the format of e, except that the sign of exponent is output by upper case letter ( E  instead of e) |
| f | double | A real value in the format [-] dddd.dddd, where dddd - one or more decimal digits. Number of displayed digits before the decimal point depends on the size of number value. Number of digits after the decimal point depends on the required accuracy. |
| g | double | A real value output in  f  or  e  format depending on what output is more compact . |
| G | double | A real value output in  F  or  E  format depending on what output is more compact . |
| a | double | A real number in format [−]0xh.hhhh  p ±dd, where h.hhhh – mantissa in the form of hexadecimal digits, using "abcdef", dd - One or more digits of exponent. Number of decimal places is determined by the  accuracy specification |
| A | double | A real number in format [−]0xh.hhhh  P ±dd, where h.hhhh – mantissa in the form of hexadecimal digits, using "ABCDEF", dd - One or more digits of exponent. Number of decimal places is determined by the  accuracy specification |
| s | string | String output |

Instead of PrintFormat() you can use printf().

Example:

```
void OnStart()
  {
//--- trade server name
   string server=AccountInfoString(ACCOUNT_SERVER);
//--- account number
   int login=(int)AccountInfoInteger(ACCOUNT_LOGIN);
//--- long value output
   long leverage=AccountInfoInteger(ACCOUNT_LEVERAGE);
   PrintFormat("%s %d: leverage = 1:%I64d",
               server,login,leverage);
//--- account currency
   string currency=AccountInfoString(ACCOUNT_CURRENCY);
//--- double value output with 2 digits after the decimal point
   double equity=AccountInfoDouble(ACCOUNT_EQUITY);
   PrintFormat("%s %d: account equity = %.2f %s",
               server,login,equity,currency);
//--- double value output with mandatory output of the +/- sign
   double profit=AccountInfoDouble(ACCOUNT_PROFIT);
   PrintFormat("%s %d: current result for open positions = %+.2f %s",
               server,login,profit,currency);
//--- double value output with variable number of digits after the decimal point
   double point_value=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
   string format_string=StringFormat("%%s: point value  = %%.%df",_Digits);
   PrintFormat(format_string,_Symbol,point_value);
//--- int value output
   int spread=(int)SymbolInfoInteger(_Symbol,SYMBOL_SPREAD);
   PrintFormat("%s: current spread in points = %d ",
               _Symbol,spread);
//--- double value output in the scientific (floating point) format with 17 meaningful digits after the decimal point
   PrintFormat("DBL_MAX = %.17e",DBL_MAX);
//--- double value output in the scientific (floating point) format with 17 meaningful digits after the decimal point
   PrintFormat("EMPTY_VALUE = %.17e",EMPTY_VALUE);
//--- output using PrintFormat() with default accuracy
   PrintFormat("PrintFormat(EMPTY_VALUE) = %e",EMPTY_VALUE);
//--- simple output using Print()
   Print("Print(EMPTY_VALUE) = ",EMPTY_VALUE);
/* execution result
   MetaQuotes-Demo 1889998: leverage = 1:100
   MetaQuotes-Demo 1889998: account equity = 22139.86 USD
   MetaQuotes-Demo 1889998: current result for open positions = +174.00 USD
   EURUSD: point value  = 0.00001
   EURUSD: current spread in points = 12 
   DBL_MAX = 1.79769313486231570e+308
   EMPTY_VALUE = 1.79769313486231570e+308
   PrintFormat(EMPTY_VALUE) = 1.797693e+308
   Print(EMPTY_VALUE) = 1.797693134862316e+308
*/
  }

```

See also

[StringFormat](/en/docs/convert/stringformat), [DoubleToString](/en/docs/convert/doubletostring), [Real types (double, float)](/en/docs/basis/types/double)
