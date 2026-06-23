# Exponential and logarithmic functions

Calculation of exponential and logarithmic functions is available in MQL5 using the corresponding API section.

The absence of the binary logarithm in the API, which is often required in computer science and combinatorics, is not a problem, since it is easy to calculate, upon request, through the available natural or decimal logarithm functions.

```
log2(x) = log(x) / log(2) = log(x) / M_LN2
log2(x) = log10(x) / log10(2)

```

Here log and log10 are available logarithmic functions (based on e and 10, respectively), M_LN2 is a built-in constant equal to log(2).

The following table lists all the constants that can be useful in logarithmic calculations.

| Constant | Description | Value |
| --- | --- | --- |
| M_E | e | 2.71828182845904523536 |
| M_LOG2E | log2(e) | 1.44269504088896340736 |
| M_LOG10E | log10(e) | 0.434294481903251827651 |
| M_LN2 | ln(2) | 0.693147180559945309417 |
| M_LN10 | ln(10) | 2.30258509299404568402 |

Examples of the functions described below are collected in the file MathExp.mq5.

double MathExp(double value) ≡ double exp(double value)

The function returns the exponent, i.e., the number e (available as a predefined constant M_E) raised to the specified power value. On overflow, the function returns inf (a kind of NaN for infinity).

```
   PRT(MathExp(0.5));      // 1.648721270700128
   PRT(MathPow(M_E, 0.5)); // 1.648721270700128
   PRT(MathExp(10000.0));  // inf, NaN

```

double MathLog(double value) ≡ double log(double value)

The function returns the natural logarithm of the passed number. If value is negative, the function returns -nan(ind) (NaN "undefined value"). If value is 0, the function returns inf (NaN "infinity").

```
   PRT(MathLog(M_E));     // 1.0
   PRT(MathLog(10000.0)); // 9.210340371976184
   PRT(MathLog(0.5));     // -0.6931471805599453
   PRT(MathLog(0.0));     // -inf, NaN
   PRT(MathLog(-0.5));    // -nan(ind)
   PRT(Log2(128));        // 7

```

The last line uses the implementation of the binary logarithm through MathLog:

```
double Log2(double value)
{
   return MathLog(value) / M_LN2;
}

```

double MathLog10(double value) ≡ double log10(double value)

The function returns the decimal logarithm of a number.

```
   PRT(MathLog10(10.0)); // 1.0
   PRT(MathLog10(10000.0)); // 4.0

```

double MathExpm1(double value) ≡ double expm1(double value)

The function returns the value of the expression (MathExp(value) - 1). In economic calculations, the function is used to calculate the effective interest (revenue or payment) per unit of time in a compound interest scheme when the number of periods tends to infinity.

```
   PRT(MathExpm1(0.1)); // 0.1051709180756476

```

double MathLog1p(double value) ≡ double log1p(double value)

The function returns the value of the expression MathLog(1 + value), i.e., it performs the opposite action to the function MathExpm1.

```
   PRT(MathLog1p(0.1)); // 0.09531017980432487

```
