# Real Types (double, float)

Real types (or floating-point types) represent values with a fractional part. In the MQL5 language there are two types for floating point numbers.The method of representation of real numbers in the computer memory is defined by the IEEE 754 standard and is independent of platforms, operating systems or programming languages.

| Type | Size in bytes | Minimal Positive Value | Maximum Value | C++ Analog |
| --- | --- | --- | --- | --- |
| float | 4 | 1.175494351e-38 | 3.402823466e+38 | float |
| double | 8 | 2.2250738585072014e-308 | 1.7976931348623158e+308 | double |

## double

[double](/en/docs/basis/types/double) real number type occupies 64 bits (1 sign bit, 11 exponent bits and 52 mantissa bits).

## float

[float](/en/docs/basis/types/double) real number type occupies 32 bits (1 sign bit, 8 exponent bits and 23 mantissa bits).

## vector

One-dimensional array of [double](/en/docs/basis/types/double) type numbers. Memory for data is allocated dynamically. Vector properties can be obtained using the [methods](/en/docs/matrix), while the vector size can be changed. The vector<double> entry can be used in template functions.

## vectorf

One-dimensional array of [float](/en/docs/basis/types/double) type numbers can be used instead of vector if the loss of precision does not matter. The vector<float> entry can be used in template functions.

## vectorc

One-dimensional array of [complex](/en/docs/basis/types/complex) type numbers is meant to handle complex numbers. The vector<complex> entry can be used in template functions. Operations on vectorc type vectors are not implemented yet.

## matrix

Matrix is a two-dimensional array of [double](/en/docs/basis/types/double) type numbers. Memory for matrix elements is distributed dynamically. Matrix properties can be obtained using the [methods](/en/docs/matrix), while the matrix shape can be changed. The matrix<double> entry can be used in template functions.

## matrixf

Two-dimensional array of [float](/en/docs/basis/types/double) type numbers can be used instead of matrix if the loss of precision does not matter. The matrix<float> entry can be used in template functions.

## matrixc

Two-dimensional array of [complex](/en/docs/basis/types/complex) type numbers is meant to handle complex numbers. The matrix<complex> entry can be used in template functions. Operations on matrixc type matrices are not implemented yet.

The double name means that the accuracy of these numbers is twice the accuracy of the float type numbers. In most cases, the double type is the most convenient one. In many cases the limited precision of float numbers is not enough. The reason why the float type is still used is saving the memory (this is important for large arrays of real numbers).

Floating-point constants consist of an integer part, a point (.) and the fractional part. The integer and fractional parts are sequences of decimal digits.

Examples:

```
   double a=12.111;
   double b=-956.1007;
   float  c =0.0001;
   float  d =16;

```

There is a scientific way of writing real constants, often this method of recording is more compact than the traditional one.

Example:

```
   double c1=1.12123515e-25;
   double c2=0.000000000000000000000000112123515; // 24 zero after the decimal point
   
   Print("1. c1 =",DoubleToString(c1,16));
   // Result: 1. c1 = 0.0000000000000000
   
   Print("2. c1 =",DoubleToString(c1,-16));
   // Result: 2. c1 = 1.1212351499999999e-025
 
   Print("3. c2 =",DoubleToString(c2,-16));
   // Result: 3. c2 = 1.1212351499999999e-025

```

It should be remembered that real numbers are stored in memory with some limited accuracy in the binary system, while generally the decimal notation is used. That's why many numbers that are precisely represented in the decimal system can be written only as an infinite fraction in the binary system.

For example, numbers 0.3 and 0.7 are represented in the computer as infinite fractions, while the number of 0.25 is stored exactly, because it represents the power of two.

In this regard, it is strongly recommended not to [compare](/en/docs/basis/operations/relation) two real numbers for equality, because such a comparison is not correct.

Example:

```
void OnStart()
  {
//---
   double three=3.0;
   double x,y,z;
   x=1/three;
   y=4/three;
   z=5/three;
   if(x+y==z) 
      Print("1/3 + 4/3 == 5/3");
   else 
      Print("1/3 + 4/3 != 5/3");
// Result: 1/3 + 4/3 != 5/3
  }

```

If you still need to compare the equality of two real numbers, then you can do this in two different ways. The first way is to compare the difference between two numbers with some small quantity that specifies the accuracy of comparison.

Example:

```
bool EqualDoubles(double d1,double d2,double epsilon)
  {
   if(epsilon<0) 
      epsilon=-epsilon;
//---
   if(d1-d2>epsilon) 
      return false;
   if(d1-d2<-epsilon) 
      return false;
//---
   return true;
  }
void OnStart()
  {
   double d_val=0.7;
   float  f_val=0.7;
   if(EqualDoubles(d_val,f_val,0.000000000000001)) 
      Print(d_val," equals ",f_val);
   else 
      Print("Different: d_val = ",DoubleToString(d_val,16),"  f_val = ",DoubleToString(f_val,16));
// Result: Different: d_val= 0.7000000000000000   f_val= 0.6999999880790710
  }

```

Note that the value of epsilon in the above example can not be less than the predefined constant DBL_EPSILON. The value of this constant is 2.2204460492503131e-016. The constant corresponding to the float type is FLT_EPSILON = 1.192092896e-07. The meaning of these values is the following: it is the lowest value that satisfies the condition  1.0 + DBL_EPSILON! = 1.0 (for numbers of float type 1.0 + FLT_EPSILON! = 1.0).

The second way offers comparing the normalized difference of two real numbers with zero. It's meaningless to compare the difference of normalized numbers with a zero, because any mathematical operation with normalized numbers gives a non-normalized result.

Example:

```
bool CompareDoubles(double number1,double number2)
  {
   if(NormalizeDouble(number1-number2,8)==0) 
      return(true);
   else 
      return(false);
  }
void OnStart()
  {
   double d_val=0.3;
   float  f_val=0.3;
   if(CompareDoubles(d_val,f_val)) 
      Print(d_val," equals ",f_val);
   else 
      Print("Different: d_val = ",DoubleToString(d_val,16),"  f_val = ",DoubleToString(f_val,16));
// Result: Different: d_val= 0.3000000000000000   f_val= 0.3000000119209290
  }

```

Some operations of the mathematical co-processor can result in the invalid real number, which can't be used in mathematical operations and operations of comparison, because the result of operations with invalid real numbers is undefined. For example, when trying to calculate the [arcsine](/en/docs/math/matharcsin) of 2, the result is the negative infinity.

Example:

```
   double abnormal = MathArcsin(2.0);
   Print("MathArcsin(2.0) =",abnormal);
// Result:  MathArcsin(2.0) = -1.#IND

```

Besides the minus infinity there is the plus infinity and NaN (not a number). To determine that this number is invalid, you can use [MathIsValidNumber()](/en/docs/math/mathisvalidnumber). According to the IEEE standard, they have a special machine representation. For example, plus infinity for the double type has the bit representation of 0x7FF0 0000 0000 0000.

Examples:

```
struct str1
  {
   double d;
  };
struct str2
  {
   long l;
  };
 
//--- Start 
   str1 s1;
   str2 s2;
//---
   s1.d=MathArcsin(2.0);        // Get the invalid number -1.#IND
   s2=s1;
   printf("1.  %f %I64X",s1.d,s2.l);
//---
   s2.l=0xFFFF000000000000;     // invalid number -1.#QNAN
   s1=s2;
   printf("2.  %f %I64X",s1.d,s2.l);
//---
   s2.l=0x7FF7000000000000;     // greatest non-number SNaN
   s1=s2;
   printf("3.   %f %I64X",s1.d,s2.l);
//---
   s2.l=0x7FF8000000000000;     // smallest non-number QNaN
   s1=s2;
   printf("4.   %f %I64X",s1.d,s2.l);
//---
   s2.l=0x7FFF000000000000;     // greatest non-number QNaN
   s1=s2;
   printf("5.   %f %I64X",s1.d,s2.l);
//---
   s2.l=0x7FF0000000000000;     // Positive infinity 1.#INF and smallest non-number SNaN
   s1=s2;
   printf("6.   %f %I64X",s1.d,s2.l);
//---
   s2.l=0xFFF0000000000000;     // Negative infinity -1.#INF
   s1=s2;
   printf("7.  %f %I64X",s1.d,s2.l);
//---
   s2.l=0x8000000000000000;     // Negative zero -0.0
   s1=s2;
   printf("8.  %f %I64X",s1.d,s2.l);
//---
   s2.l=0x3FE0000000000000;     // 0.5
   s1=s2;
   printf("9.   %f %I64X",s1.d,s2.l);
//---
   s2.l=0x3FF0000000000000;     // 1.0
   s1=s2;
   printf("10.  %f %I64X",s1.d,s2.l);
//---
   s2.l=0x7FEFFFFFFFFFFFFF;     // Greatest normalized number (MAX_DBL)
   s1=s2;
   printf("11.  %.16e %I64X",s1.d,s2.l);
//---
   s2.l=0x0010000000000000;     // Smallest positive normalized (MIN_DBL)
   s1=s2;
   printf("12.  %.16e %.16I64X",s1.d,s2.l);
//---
   s1.d=0.7;                    // Show that the number of 0.7 - endless fraction
   s2=s1;
   printf("13.  %.16e %.16I64X",s1.d,s2.l);
/*
1.  -1.#IND00 FFF8000000000000
2.  -1.#QNAN0 FFFF000000000000
3.   1.#SNAN0 7FF7000000000000
4.   1.#QNAN0 7FF8000000000000
5.   1.#QNAN0 7FFF000000000000
6.   1.#INF00 7FF0000000000000
7.  -1.#INF00 FFF0000000000000
8.  -0.000000 8000000000000000
9.   0.500000 3FE0000000000000
10.  1.000000 3FF0000000000000
11.  1.7976931348623157e+308 7FEFFFFFFFFFFFFF
12.  2.2250738585072014e-308 0010000000000000
13.  6.9999999999999996e-001 3FE6666666666666 
*/

```

See also

[DoubleToString](/en/docs/convert/doubletostring), [NormalizeDouble](/en/docs/convert/normalizedouble), [Numeric Type Constants](/en/docs/constants/namedconstants/typeconstants)
