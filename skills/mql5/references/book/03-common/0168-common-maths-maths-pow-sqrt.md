# Powers and roots

The MQL5 API provides a generic function MathPow for raising a number to an arbitrary power, as well as a function for a special case with a power of 0.5, more familiar to us as the operation of extracting a square root MathSqrt.

To test the functions, use the MathPowSqrt.mq5 script.

double MathPow(double base, double exponent) ≡ double pow(double base, double exponent)

The function raises the base to the specified power exponent.

```
   PRT(MathPow(2.0, 1.5));  // 2.82842712474619
   PRT(MathPow(2.0, -1.5)); // 0.3535533905932738
   PRT(MathPow(2.0, 0.5));  // 1.414213562373095

```

double MathSqrt(double value) ≡ double sqrt(double value)

The function returns the square root of a number.

```
   PRT(MathSqrt(2.0));      // 1.414213562373095
   PRT(MathSqrt(-2.0));     // -nan(ind)

```

MQL5 defines several constants containing ready-made calculation values involving sqrt.

| Constant | Description | Value |
| --- | --- | --- |
| M_SQRT2 | sqrt(2.0) | 1.41421356237309504880 |
| M_SQRT1_2 | 1 / sqrt(2.0) | 0.707106781186547524401 |
| M_2_SQRTPI | 2.0 / sqrt(M_PI) | 1.12837916709551257390 |

Here M_PI is the Pi number (π=3.14159265358979323846, see further along the section [Trigonometric functions](/en/book/common/maths/maths_trig)).

All built-in constants are described in the [documentation](https://www.mql5.com/en/docs/constants/namedconstants/mathsconstants).
