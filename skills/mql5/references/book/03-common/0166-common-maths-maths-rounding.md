# Rounding functions

The MQL5 API includes several functions for rounding numbers to the nearest integer (in one direction or another). Despite the rounding operation, all functions return a number of type double (with an empty fractional part).

From a technical point of view, they accept arguments of any numeric type, but only real numbers are rounded, and integers are only converted to double.

If you want to round up to a specific sign, use NormalizeDouble (see section [Normalization of doubles](/en/book/common/conversions/conversions_normalize)).

Examples of working with functions are given in the file MathRound.mq5.

double MathRound(numeric value) ≡ double round(numeric value)

The function rounds a number up or down to the nearest integer.

```
   PRT((MathRound(5.5)));  // 6.0
   PRT((MathRound(-5.5))); // -6.0
   PRT((MathRound(11)));   // 11.0
   PRT((MathRound(-11)));  // -11.0

```

If the value of the fractional part is greater than or equal to 0.5, the mantissa is increased by one (regardless of the sign of the number).

double MathCeil(numeric value) ≡ double ceil(numeric value)

double MathFloor(numeric value) ≡ double floor(numeric value)

The functions return the closest greater integer value (for ceil) or closest lower integer value (for floor) to the transferred value. If value is already equal to an integer (has a zero fractional part), this integer is returned.

```
   PRT((MathCeil(5.5)));   // 6.0
   PRT((MathCeil(-5.5)));  // -5.0
   PRT((MathFloor(5.5)));  // 5.0
   PRT((MathFloor(-5.5))); // -6.0
   PRT((MathCeil(11)));    // 11.0
   PRT((MathCeil(-11)));   // -11.0
   PRT((MathFloor(11)));   // 11.0
   PRT((MathFloor(-11)));  // -11.0

```
