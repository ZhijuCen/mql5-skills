# Normalization of doubles

The MQL5 API provides a function for rounding floating point numbers to a specified precision (the number of significant digits in the fractional part).

double NormalizeDouble(double number, int digits)

Rounding is required in trading algorithms to set volumes and prices in [orders](/en/book/automation/experts/experts_mqltraderequest). Rounding is performed according to the standard rules: the last visible digit is increased by 1 if the next (discarded) digit is greater than or equal to 5.

Valid values of the parameter digits: 0 to 8.

Examples of using the function are available in the ConversionNormal.mq5 file.

```
void OnStart()
{
   Print(M_PI);                      // 3.141592653589793
   Print(NormalizeDouble(M_PI, 16)); // 3.14159265359
   Print(NormalizeDouble(M_PI, 8));  // 3.14159265
   Print(NormalizeDouble(M_PI, 5));  // 3.14159
   Print(NormalizeDouble(M_PI, 1));  // 3.1
   Print(NormalizeDouble(M_PI, -1)); // 3.14159265359
   ...

```

Due to the fact that any real number has a limited [internal representation](/en/book/basis/builtin_types/float_numbers) precision, the number can be displayed approximately even when normalized:

```
   ...
   Print(512.06);                    // 512.0599999999999
   Print(NormalizeDouble(512.06, 5));// 512.0599999999999
   Print(DoubleToString(512.06, 5)); // 512.06000000
   Print((float)512.06);             // 512.06
}

```

This is normal and inevitable. For more compact formatting, use the functions [DoubleToString](/en/book/common/conversions/conversions_numbers), [StringFormat](/en/book/common/strings/strings_format) or intermediate casting to (float).

To round a number up or down to the nearest integer, use the functions MathRound, MathCeil, MathFloor (see section [Rounding functions](/en/book/common/maths/maths_rounding)).
