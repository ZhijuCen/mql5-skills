# Remainder after division (Modulo operation)

To divide integers with remainder, MQL5 has the built-in modulo operator '%', described in the section [Arithmetic operations](/en/book/basis/expressions/operators_arithmetic). However, this operator is not applicable to real numbers. In the case when the divisor, the dividend, or both operands are real, you should use the function MathMod (or short form fmod).

double MathMod(double dividend, double divider) ≡ double fmod(double dividend, double divider)

The function returns the real remainder after dividing the first passed number (dividend) by the second (divider).

If any argument is negative, the sign of the result is determined by the rules described in the above [section](/en/book/basis/expressions/operators_arithmetic).

Examples of how the function works are available in the script MathMod.mq5.

```
   PRT(MathMod(10.0, 3));     // 1.0
   PRT(MathMod(10.0, 3.5));   // 3.0
   PRT(MathMod(10.0, 3.49));  // 3.02
   PRT(MathMod(10.0, M_PI));  // 0.5752220392306207
   PRT(MathMod(10.0, -1.5));  // 1.0, the sign is gone
   PRT(MathMod(-10.0, -1.5)); // -1.0

```
