# Mathematical Constants

Special constants containing values are reserved for some mathematical expressions. These constants can be used in any place of the program instead of calculating their values using [mathematical functions](/en/docs/math).

| Constant | Description | Value |
| --- | --- | --- |
| M_E | e | 2.71828182845904523536 |
| M_LOG2E | log2(e) | 1.44269504088896340736 |
| M_LOG10E | log10(e) | 0.434294481903251827651 |
| M_LN2 | ln(2) | 0.693147180559945309417 |
| M_LN10 | ln(10) | 2.30258509299404568402 |
| M_PI | pi | 3.14159265358979323846 |
| M_PI_2 | pi/2 | 1.57079632679489661923 |
| M_PI_4 | pi/4 | 0.785398163397448309616 |
| M_1_PI | 1/pi | 0.318309886183790671538 |
| M_2_PI | 2/pi | 0.636619772367581343076 |
| M_2_SQRTPI | 2/sqrt(pi) | 1.12837916709551257390 |
| M_SQRT2 | sqrt(2) | 1.41421356237309504880 |
| M_SQRT1_2 | 1/sqrt(2) | 0.707106781186547524401 |

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- print the values of constants
   Print("M_E = ",DoubleToString(M_E,16));
   Print("M_LOG2E = ",DoubleToString(M_LOG2E,16));
   Print("M_LOG10E = ",DoubleToString(M_LOG10E,16));
   Print("M_LN2 = ",DoubleToString(M_LN2,16));
   Print("M_LN10 = ",DoubleToString(M_LN10,16));
   Print("M_PI = ",DoubleToString(M_PI,16));
   Print("M_PI_2 = ",DoubleToString(M_PI_2,16));
   Print("M_PI_4 = ",DoubleToString(M_PI_4,16));
   Print("M_1_PI = ",DoubleToString(M_1_PI,16));
   Print("M_2_PI = ",DoubleToString(M_2_PI,16));
   Print("M_2_SQRTPI = ",DoubleToString(M_2_SQRTPI,16));
   Print("M_SQRT2 = ",DoubleToString(M_SQRT2,16));
   Print("M_SQRT1_2 = ",DoubleToString(M_SQRT1_2,16));
  }

```
