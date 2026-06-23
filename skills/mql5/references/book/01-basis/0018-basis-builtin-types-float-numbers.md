# Floating-point numbers

We use numbers with a decimal point, or real numbers, in everyday life just as often as integers. The name 'real' itself indicates that using such numbers, you can express something tangible from the real world, such as weight, length, body temperature, i.e., everything that can be measured by a non-integer amount of units, but with "a little more."

We often use real numbers in trading, too. For instance, they are used to express symbol prices or volumes in trading orders (normally permitting the fractional parts of a full-sized lot).

There are 2 real types provided in MQL5: float for normal accuracy and double for double accuracy.

In the source code, the constant values of types float and double are usually recorded as an integer and a fractional part (each being a sequence of digits), separated by the character '.', such as 1.23 or -789.01. There can be no integer or fraction (but not both at a time), but the point is mandatory. For instance, .123 means 0.123, while 123. means 123.0. Simply 123 will create a constant of integer type.

However, there is another form of recording real constants, the exponential one. In it, the integer and fractional part are followed by 'E' or 'e' (case does not matter) and an integer representing the power, to which 10 should be raised to obtain an additional factor. For instance, the following representations display the same number, 0.57, in exponential form:

```
 .0057e2
0.057e1
.057e1
57e-2

```

When recording real constants, the latter ones are defined by default as type double (they consume 8 bytes). To set type float, suffix 'F' (or 'f') should be added to the constant on the right.

Types float and double differ by their sizes, ranges of values, and number representation accuracy. All this is shown in the table below.

| Type | Size (bytes) | Minimum | Maximum | Accuracy (digit orders) |
| --- | --- | --- | --- | --- |
| float | 4 | ±1.18 * 10 -38 | ±3.4 * 10 38 | 6-9, usually 7 |
| double | 8 | ±2.23 * 10 -308 | ±1.80 * 10 308 | 15-18, usually 16 |

Range of values is shown for them in absolute terms: Minimum and maximum determine the amplitude of permitted values in both positive and negative regions. Similar to integer types, there are embedded named constants for these limiting values: FLT_MIN, FLT_MAX, DBL_MIN, DBL_MAX.

Please note that real numbers are always signed, that is, there are no unsigned analogs for them.

Accuracy shall mean the quantity of significant digits (decimal digits) the real number of the relevant type is able to store undistorted.

Indeed, the numbers of real types are not as accurate as those of integer types. This is the price to be paid for their universality and a much wider range of potential values. For instance, if an unsigned 4-byte integer (uint) has the highest value of 4294967295, i.e., about 4 million, or 4.29*109, then the 4-byte real one (float) has 3.4 * 1038, which is by 29 orders of magnitude higher. For 8-byte types, the difference is even more perceptible: ulong can house 18446744073709551615 (18.44*1018, or ~18 quintillion), while double can house 1.80 * 10308, that is, by 289 orders of magnitude more. Insertion provides more detail regarding accuracy.

Mantissa and Exponent  

   

The internal representation of real numbers in memory (in the bytes allocated for them) is quite tricky. The higher-order bit is used as a marker of the negative sign (we have also seen that in integer types). All other bits are divided into two groups. The larger one contains the mantissa of the number, i.e., significant digits (we mean binary digits, i.e., bits). The smaller one stores the power (exponent), to which 10 must be raised to obtain the stored number upon multiplying it by the mantissa. Particularly, for type float mantissa is sized 24 bits (FLT_MANT_DIG), while for double it is 53 (DBL_MANT_DIG). In terms of conventional decimal places (digits), we will get the same accuracy that has been shown in the table above: 6 (FLT_DIG) is the lowest quantity of significant digits for float, while 15 (DBL_DIG) is that for double. However, depending on the particular number, it can have "lucky" combinations of bits, corresponding to a greater quantity of decimal digits. Sizes of the parameters are 8 and 11 bits for float and double, respectively.  

   

Due to the exponent, real numbers get a much larger range of values. At the same time, with the increase in the exponent, the "specific weight" of the low-order digit of mantissa increases, too. This means that two neighboring real numbers that can be represented in the computer memory are substantially different. For instance, for number 1.0 the "specific weight" of the low-order bit is 1.192092896e—07 (FLT_EPSILON) in case of float and 2.2204460492503131e-016 (DBL_EPSILON) in case of double. In other words, 1.0 is indistinguishable from any number near it if such a number is below 1.192092896e—07. This may seem not very important or "not a big deal," but this uncertainty region gets larger for larger numbers. If you store in float a number about 1 billion (1*109), the last 2 digits will stop being safely stored or restored from memory (see the code sample below). However, basically, the problem is not the absolute value of a number, but the maximum quantity of digits in it, which should be recalled without losses. Equally "well," we can try to fit a number represented as 1234.56789 (which is structurally much like the price of a financial instrument) in float; and its two last digits will "float" due to the lack of accuracy in their internal representation.  

   

For double, a similar situation will start showing for much greater numbers (or for a much greater quantity of significant digits), but it is still possible and often happens in practice. You should consider this when operating very large or very small real numbers and write your programs with additional checks for potential loss of accuracy. In particular, you should compare a real number with zero in a special manner. We will deal with it in the section on [comparison operators](/en/book/basis/expressions/operators_relational).   

   

It may seem to a careful reader that the sizes of mantissa and exponent above are specified wrongly. Let's explain that exemplified by float. It is stored in the memory cell sized 4 bytes, that is, consumes 32 bits. At the same time, the sizes of mantissa (24) and exponent (8) sum to 32 already. Then where is the signed bit? The matter is that IT professionals arranged to store mantissa in the 'normalized' form. It will be easier to understand what it is if we consider the exponential form of recording a normal decimal number first. Let's say number 123.0 could be represented as 1.23E2, 12.3E1, or 0.123E3. A designation is considered to be the normalized form, where only one significant digit (i.e., not zero) is placed before the point. For this number, it is 1.23E2. By definition, digits from 1 through 9 are considered significant digits in decimal notation. Now we are smoothly going to the binary notation. There is only one significant digit in it, 1. It appears that the normalized form in binary notation always starts with 1, and it can be omitted (not to spend memory on it). In this manner, one bit can be saved in the mantissa. In fact, it contains 23 bits (one more higher-order unity is implicit and added automatically when reconstructing the number and retrieving it from memory). Reducing mantissa by 1 bit makes room for the signed bit.

Predominantly, where the floating-point type should be used, we choose double as a more accurate one. Type float is only used to save memory, such as when working with very large data arrays.

Some examples of using the constants of real types are shown in script MQL5/Scripts/MQL5Book/p2/TypeFloat.mq5.

```
void OnStart()
{
  double a0 = 123;      // ok, a0 = 123.0
  double a1 = 123.0;    // ok, a1 = 123.0
  double a2 = 0.123E3;  // ok, a2 = 123.0
  double a3 = 12300E-2; // ok, a3 = 123.0
  double b = -.75;      // ok, b = -0.75
  double q = LONG_MAX;  // warning: truncation, q = 9.223372036854776e+18
                        //               LONG_MAX = 9223372036854775807
  double d = 9007199254740992; // ok, maximal stable long in double
  double z = 0.12345678901234567890123456789; // ok, but truncated
                           // to 16 digits: z = 0.1234567890123457
  double y1 = 1234.56789;  // ok, y1 = 1234.56789
  double y2 = 1234.56789f; // accuracy loss, y2 = 1234.56787109375
  float m = 1000000000.0;  // ok, stored as is
  float n =  999999975.0;  // warning: truncation, n = 1000000000.0
}

```

Variables a0, a1, a2, and a3 contain the same numbers (123.0) written in different methods.

In the constant for variable b, the insignificant zero is omitted before the point. Moreover, here is the demonstration of recording a negative number using the minus sign, '-'.

An attempt is made to store the greatest integer in variable q. At this place, the compiler gives a warning, because double cannot represent LONG_MAX accurately: Instead of 9223372036854775807, there will be 9223372036854776000. It obviously demonstrates that, even though the ranges of the double values exceed those of integers vastly, it is achieved due to losing the low-order digits.

As a comparison, the maximum integer that the double type is able to store without any distortions is given as the value of variable d. In the sequence of integers, it will be followed by sporadic skips, if we use double for them.

Variable z reminds us again about the limitation on the maximum quantity of significant digits (16) – a longer constant will be truncated.

Variables y1 and y2, in which the same number is recorded in different formats (double and float), allow seeing the loss of accuracy due to the transition to float.

In fact, variables m and n will be equal, because 999999975.0 is roughly stored in the internal representation and turns into 1000000000.0.

Numeric types are often used to calculate using formulas; a wide set of operations is defined for them (see [Expressions](/en/book/basis/expressions)).

Computations can sometimes lead to incorrect results, that is, they cannot be represented as a number. For example, the root of a negative number or the logarithm of zero cannot be defined. In such cases, real types can store a special value named NaN (Not A Number). In fact, there are several different types of such values that allow, for instance, telling the difference between plus infinity and minus infinity. MQL5 provides a special function, MathIsValidNumber, that checks whether the double value is a number or one of NaN values.
