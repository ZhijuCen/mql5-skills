# MathClassify

Determines the type of a real number and returns a result as a value from the [ENUM_FP_CLASS](/en/docs/math/mathclassify#enum_fp_class) enumeration

```
ENUM_FP_CLASS  MathClassify(
   double  value      // real number
   );

```

Parameters

value

[in]  The real number to be checked

Return Value

A value from the ENUM_FP_CLASS enumeration

ENUM_FP_CLASS

| ID | Description |
| --- | --- |
| FP_SUBNORMAL | A subnormal number which is closer to zero than the smallest representable normal number DBL_MIN (2.2250738585072014e-308) |
| FP_NORMAL | A normal number in the range between 2.2250738585072014e-308 and 1.7976931348623158e+308 |
| FP_ZERO | A positive or a negative zero |
| FP_INFINITE | A number which cannot be represented by the appropriate type, positive or negative infinity |
| FP_NAN | Not a number. |

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
 {
//--- test NaN
  double nan=double("nan");
  PrintFormat("Test NaN: %G is %s, MathIsValidNumber(NaN)=%s",
              nan,
              EnumToString(MathClassify(nan)),
              (string)MathIsValidNumber(nan));
//--- test infinity
  double inf=double("inf");
  PrintFormat("Test Inf: %G is %s, MathIsValidNumber(inf)=%s",
              inf,
              EnumToString(MathClassify(inf)),
              (string)MathIsValidNumber(inf));
//--- test normal value
  double normal=1.2345e6;
  PrintFormat("Test Normal: %G is %s, MathIsValidNumber(normal)=%s",
              normal,
              EnumToString(MathClassify(normal)),
              (string)MathIsValidNumber(normal));
//--- test subnormal value
  double sub_normal=DBL_MIN/2.0;
  PrintFormat("Test Subnormal: %G is %s, MathIsValidNumber(sub_normal)=%s",
              sub_normal,
              EnumToString(MathClassify(sub_normal)),
              (string)MathIsValidNumber(sub_normal));
//--- test zero value
  double zero=0.0/(-1);
  PrintFormat("Test Zero: %G is %s, MathIsValidNumber(zero)=%s",
              zero,
              EnumToString(MathClassify(zero)),
              (string)MathIsValidNumber(zero));
 } 
 /*
 Result:
   Test NaN: NAN is FP_NAN, MathIsValidNumber(NaN)=false
   Test Inf: INF is FP_INFINITE, MathIsValidNumber(inf)=false
   Test Normal: 1.2345E+06 is FP_NORMAL, MathIsValidNumber(normal)=true
   Test Subnormal: 1.11254E-308 is FP_SUBNORMAL, MathIsValidNumber(sub_normal)=true
   Test Zero: -0 is FP_ZERO, MathIsValidNumber(zero)=true
*/ 
//+------------------------------------------------------------------+

```

See also

[Real types (double, float)](/en/docs/basis/types/double), [MathIsValidNumber](/en/docs/math/mathisvalidnumber)
