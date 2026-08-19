# StringToInteger

The function converts string containing a symbol representation of number into number of long (integer) type.

```
long  StringToInteger(
   string  value      // string
   );

```

Parameters

value

[in]  String containing a number.

Return Value

Value of long type.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- string to convert
   string str = "12345.54321";
//--- convert the input string as a number into a long type variable
   long converted=StringToInteger(str);
//--- display the obtained number in the journal with the fractional part cut off
   PrintFormat("The string '%s' is converted to the integer number %I64d", str, converted);
   /*
   result:
   The string '12345.54321' is converted to the integer number 12345
   */
  }

```

See also

[IntegerToString](/en/docs/convert/integertostring), [Real types (double, float)](/en/docs/basis/types/double), [Typecasting](/en/docs/basis/types/casting)
