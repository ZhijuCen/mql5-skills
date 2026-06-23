# DoubleToString

Converting numeric value into text string.

```
string  DoubleToString(
   double  value,      // number
   int     digits=8    // number of digits after decimal point
   );

```

Parameters

value

[in]  Value with a floating point.

digits

[in]  Accuracy format. If the digits value is in the range between 0 and 16, a string presentation of a number with the specified number of digits after the point will be obtained. If the digits value is in the range between -1 and -16, a string representation of a number in the scientific format with the specified number of digits after the decimal point will be obtained. In all other cases the string value will contain 8 digits after the decimal point.

Return Value

String containing a symbol representation of a number with the specified accuracy.

Example:

```
   Print("DoubleToString(120.0 + M_PI) : ",DoubleToString(120.0+M_PI));
   Print("DoubleToString(120.0 + M_PI,16) : ",DoubleToString(120.0+M_PI,16));
   Print("DoubleToString(120.0 + M_PI,-16) : ",DoubleToString(120.0+M_PI,-16));
   Print("DoubleToString(120.0 + M_PI,-1) : ",DoubleToString(120.0+M_PI,-1));
   Print("DoubleToString(120.0 + M_PI,-20) : ",DoubleToString(120.0+M_PI,-20));

```

See also

[NormalizeDouble](/en/docs/convert/normalizedouble), [StringToDouble](/en/docs/convert/stringtodouble)
