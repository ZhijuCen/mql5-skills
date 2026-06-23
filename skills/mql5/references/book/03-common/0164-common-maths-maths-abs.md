# The absolute value of a number

The MQL5 API provides the MathAbs function which can remove the minus sign from the number if it exists. Therefore, there is no need to manually code longer equivalents like this:

```
if(x < 0) x = -x;

```

numeric MathAbs(numeric value) ≡ numeric fabs(numeric value)

The function returns the absolute value of the number passed to it, i.e., its modulus. The argument can be a number of any type. In other words, the function is overloaded for char/uchar, short/ushort, int/uint, long/ulong, float and double, although for unsigned types the values are always non-negative.

When passing a string, it will be implicitly converted to a double number, and the compiler will generate a relevant warning.

The type of the return value is always the same as the type of the argument, and therefore the compiler may need to cast the value to the receiving variable type if the types are different.

Function usage examples are available in the MathAbs.mq5 file.

```
void OnStart()
{
   double x = 123.45;
   double y = -123.45;
   int i = -1;
   
   PRT(MathAbs(x)); // 123.45, number left "as is"
   PRT(MathAbs(y)); // 123.45, minus sign gone 
   PRT(MathAbs(i)); // 1, int is handled naturally
   
   int k = MathAbs(i);  // no warning: type int for parameter and result
   
   // situations with warnings:
   // double to long conversion required
   long j = MathAbs(x); // possible loss of data due to type conversion
   
   // need to be converted from large type (4 bytes) to small type (2 bytes)
   short c = MathAbs(i); // possible loss of data due to type conversion
   ...

```

It's important to note that converting a signed integer to an unsigned integer is not equivalent to taking the modulus of a number:

```
   uint u_cast = i;
   uint u_abs = MathAbs(i);
   PRT(u_cast);             // 4294967295, 0xFFFFFFFF
   PRT(u_abs);              // 1

```

Also note that the number 0 can have a sign:

```
   ...
   double n = 0;
   double z = i * n;
   PRT(z);               // -0.0
   PRT(MathAbs(z));      //  0.0
   PRT(z == MathAbs(z)); // true
}

```

One of the best examples of how to use MathAbs is to test two real numbers for equality. As is known, real numbers have a limited accuracy of representing values, which can further degrade in the course of lengthy calculations (for example, the sum of ten values 0.1 does not give exactly 1.0). Strict condition value1 == value2 can give false in most cases, when purely speculative equality should hold.

Therefore, to compare real values, the following notation is usually used:

```
MathAbs(value1 - value2) < EPS

```

where EPS is a small positive value which indicates a precision (see an example in the [Comparison operations](/en/book/basis/expressions/operators_relational) section).
