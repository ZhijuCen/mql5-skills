# Numerical Type Constants

Each simple numerical type is intended for a certain type of tasks and allows optimizing the operation of a mql5-program when used correctly. For a better code readability and correct handling of calculation results, there are constants which allow to receive information about restrictions set to a certain type of simple data.

| Constant | Description | Value |
| --- | --- | --- |
| CHAR_MIN | Minimal value, which can be represented by char type | -128 |
| CHAR_MAX | Maximal value, which can be represented by char type | 127 |
| UCHAR_MAX | Maximal value, which can be represented by uchar type | 255 |
| SHORT_MIN | Minimal value, which can be represented by short type | -32768 |
| SHORT_MAX | Maximal value, which can be represented by short type | 32767 |
| USHORT_MAX | Maximal value, which can be represented by ushort type | 65535 |
| INT_MIN | Minimal value, which can be represented by int type | -2147483648 |
| INT_MAX | Maximal value, which can be represented by int type | 2147483647 |
| UINT_MAX | Maximal value, which can be represented by uint type | 4294967295 |
| LONG_MIN | Minimal value, which can be represented by long type | -9223372036854775808 |
| LONG_MAX | Maximal value, which can be represented by long type | 9223372036854775807 |
| ULONG_MAX | Maximal value, which can be represented by ulong type | 18446744073709551615 |
| DBL_MIN | Minimal positive value, which can be represented by double type | 2.2250738585072014e-308 |
| DBL_MAX | Maximal value, which can be represented by double type | 1.7976931348623158e+308 |
| DBL_EPSILON | Minimal value, which satisfies the condition: 
 1.0+DBL_EPSILON != 1.0 (for double type) | 2.2204460492503131e-016 |
| DBL_DIG | Number of significant decimal digits for double type | 15 |
| DBL_MANT_DIG | Number of bits in a mantissa for double type | 53 |
| DBL_MAX_10_EXP | Maximal decimal value of exponent degree for double type | 308 |
| DBL_MAX_EXP | Maximal binary value of exponent degree for double type | 1024 |
| DBL_MIN_10_EXP | Minimal decimal value of exponent degree for double type | (-307) |
| DBL_MIN_EXP | Minimal binary value of exponent degree for double type | (-1021) |
| FLT_MIN | Minimal positive value, which can be represented by float type | 1.175494351e-38 |
| FLT_MAX | Maximal value, which can be represented by float type | 3.402823466e+38 |
| FLT_EPSILON | Minimal value, which satisfies the condition: 
 1.0+DBL_EPSILON != 1.0 (for float type) | 1.192092896e–07 |
| FLT_DIG | Number of significant decimal digits for float type | 6 |
| FLT_MANT_DIG | Number of bits in a mantissa for float type | 24 |
| FLT_MAX_10_EXP | Maximal decimal value of exponent degree for float type | 38 |
| FLT_MAX_EXP | Maximal binary value of exponent degree for float type | 128 |
| FLT_MIN_10_EXP | Minimal decimal value of exponent degree for float type | -37 |
| FLT_MIN_EXP | Minimal binary value of exponent degree for float type | (-125) |

Example:

```
void OnStart()
  {
//--- print the constant values
   printf("CHAR_MIN = %d",CHAR_MIN);
   printf("CHAR_MAX = %d",CHAR_MAX);
   printf("UCHAR_MAX = %d",UCHAR_MAX);
   printf("SHORT_MIN = %d",SHORT_MIN);
   printf("SHORT_MAX = %d",SHORT_MAX);
   printf("USHORT_MAX = %d",USHORT_MAX);
   printf("INT_MIN = %d",INT_MIN);
   printf("INT_MAX = %d",INT_MAX);
   printf("UINT_MAX = %u",UINT_MAX);
   printf("LONG_MIN = %I64d",LONG_MIN);
   printf("LONG_MAX = %I64d",LONG_MAX);
   printf("ULONG_MAX = %I64u",ULONG_MAX);
   printf("EMPTY_VALUE = %.16e",EMPTY_VALUE);
   printf("DBL_MIN = %.16e",DBL_MIN);
   printf("DBL_MAX = %.16e",DBL_MAX);
   printf("DBL_EPSILON = %.16e",DBL_EPSILON);
   printf("DBL_DIG = %d",DBL_DIG);
   printf("DBL_MANT_DIG = %d",DBL_MANT_DIG);
   printf("DBL_MAX_10_EXP =  %d",DBL_MAX_10_EXP);
   printf("DBL_MAX_EXP = %d",DBL_MAX_EXP);
   printf("DBL_MIN_10_EXP = %d",DBL_MIN_10_EXP);
   printf("DBL_MIN_EXP = %d",DBL_MIN_EXP);
   printf("FLT_MIN = %.8e",FLT_MIN);
   printf("FLT_MAX = %.8e",FLT_MAX);
   printf("FLT_EPSILON = %.8e",FLT_EPSILON);
/*
   CHAR_MIN = -128
   CHAR_MAX = 127
   UCHAR_MAX = 255
   SHORT_MIN = -32768
   SHORT_MAX = 32767
   USHORT_MAX = 65535
   INT_MIN = -2147483648
   INT_MAX = 2147483647
   UINT_MAX = 4294967295
   LONG_MIN = -9223372036854775808
   LONG_MAX = 9223372036854775807
   ULONG_MAX = 18446744073709551615
   EMPTY_VALUE = 1.7976931348623157e+308
   DBL_MIN = 2.2250738585072014e-308
   DBL_MAX = 1.7976931348623157e+308
   DBL_EPSILON = 2.2204460492503131e-16
   DBL_DIG = 15
   DBL_MANT_DIG = 53
   DBL_MAX_10_EXP =  308
   DBL_MAX_EXP = 1024
   DBL_MIN_10_EXP = -307
   DBL_MIN_EXP = -1021
   FLT_MIN = 1.17549435e-38
   FLT_MAX = 3.40282347e+38
   FLT_EPSILON = 1.19209290e-07
*/ 
  }

```
