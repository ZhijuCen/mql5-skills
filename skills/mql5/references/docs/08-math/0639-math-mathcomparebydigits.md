# MathCompareByDigits

Compares two numbers for equality to the specified number of significant digits.

```
bool MathCompareByDigits(
 const double value1, // first number
 const double value2, // second number
 const int digits // number of significant digits
 );
 
bool MathCompareByDigits(
 const float value1, // first number
 const float value2, // second number
 const int digits // number of significant digits
 );
 
bool MathCompareByDigits(
 const complex value1, // first number
 const complex value2, // second number
 const int digits // number of significant digits
 );
 
bool MathCompareByDigits(
 const complexf value1, // first number
 const complexf value2, // second number
 const int digits // number of significant digits
 );

```

Parameters

value1

[in] First number to compare.

value2

[in] Second number to compare.

digits

[in] Number of significant digits to compare.

Return Value

Returns true if the compared numbers match to digits significant digits. Otherwise, returns false.

Note

The function is useful when the order of magnitude of the compared numbers is not known in advance, and also for complex numbers whose real and imaginary parts can differ significantly in magnitude. In other cases, it is better to use epsilon-based comparison.

If one of the values is 0, comparison is not performed. In this case, use epsilon-based comparison. For complex numbers, real and imaginary parts are compared pairwise.
