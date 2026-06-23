# Integers

Integer types are intended for storing numbers without decimal points. They should be chosen if the applied sense of the value excludes fractions. For example, the numbers of bars on a chart or of open positions are always integers.

MQL5 allows choosing integer types sized 1-8 bytes using keywords char, short, int, and long, respectively. They all are the signed types, i.e., they can contain both positive and negative values. If necessary, integer types having the same sizes can be declared unsigned (their names starting with 'u' for 'unsigned'): uchar, ushort, uint, and ulong.

Based on the type size and being signed/unsigned, the following table shows the ranges of potential values.

| Type | min | max |
| --- | --- | --- |
| char | -128 | 127 |
| uchar | 0 | 255 |
| short | -32768 | 32767 |
| ushort | 0 | 65535 |
| int | -2147483648 | 2147483647 |
| uint | 0 | 4294967295 |
| long | -9223372036854775808 | 9223372036854775807 |
| ulong | 0 | 18446744073709551615 |

There is no need to memorize the above limiting values for each integer. There are many predefined named constants in MQL5, which can be used in a code instead of 'magic' numbers, including the lowest/highest integers. This technology is considered in a section dealing with the [preprocessor](/en/book/basis/preprocessor/preprocessor_define_simple). Here, we just list the relevant named constants: CHAR_MIN, CHAR_MAX, UCHAR_MAX, SHORT_MIN, SHORT_MAX,USHORT_MAX, INT_MIN, INT_MAX, UINT_MAX, LONG_MIN, LONG_MAX, and ULONG_MAX.

Let's explain how these values are obtained. This requires returning to bits and bytes.

The number of all possible combinations of different states of 8 bits, enabled and disabled, within one byte, is 256. This produces the range of values 0-255 that can be stored in a byte. However, interpreting them depends on the type, for which this byte is allocated. Different interpretations are ensured by the compiler, according to the programmer's statements.

The low-order (rightmost) bit in a byte means 1, the second 2, the third 4, and so on through the high-order bit that means 128. It's plain to see that these numbers are equal to two raised to a power equaling the bit number (numbering starts from 0). This is the effect of using the binary system.

| Bits | high-order | low-order |
| --- | --- | --- |
| Number | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
| Value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

Where all bits are set, this produces the sum of all powers of two, i.e., 255 is the highest value for a byte. If all bits are reset, we get zero. If a low-order bit is enabled, the number is odd.

In coding signed numbers, the high-order bit is used to mark negative values. Therefore, for a single-byte integer within the positive range, 127 becomes the highest value. For negative values, there are 128 possible combinations, i.e., the lowest value is -128. Where all bits in a byte are set, it is interpreted as -1. If the lower-order bit is reset in such a number, we will get -2, etc. If only the higher-order bit (sign) is set and all other bits are reset, we get -128.

This coding that may seem to be irrational is called "additional." It allows you to unify computations of signed and unsigned numbers at the hardware level. Moreover, it allows you not to lose one value, which would happen if the positive and negative regions were coded identically: Then we would have got two values for zero, i.e., a positive 0 and a negative 0. What is more, this would bring ambiguity.

Numbers with more bytes, i.e., 2, 4, or 8, have a similar consecutive numbering of bits and the progression of their respective values. In all cases, a criterion for the number negativity is the set high-order bit of the high-order byte.

Thus, we can use a byte to store an unsigned integer (uchar, i.e., unsigned character abbreviated) within the range of 0-255. We can also write a signed integer into the byte (for which purpose we will describe its type as char). In this case, the compiler will divide the available amount of combinations of 256 equally between positive and negative values, having displayed it onto the region from -128 through 127 (the 256th value is zero). It's plain to see that values 0-127 will be coded equally at the bit level for signed and unsigned bytes. However, large absolute values, starting from 128, will turn into negative ones (according to the scheme described in the insertion above). This "transformation" only takes place at the moment of reading or performing any operations with the value stored, with the identical internal data representation (state of bits).

We will consider this matter in more detail in the section dealing with [typecasting](/en/book/basis/conversion).

In a similar manner as with single-byte integers, it is easy to calculate that the number of bit combinations is 65536 for 2 bytes. Hence, the ranges are formed for the signed and unsigned two-byte integer, short and ushort. Other types allow storing even larger values due to increasing their byte sizes.

Please note that using an unsigned type with the same size allows doubling the highest positive value. This may be necessary for storing potentially very large quantities, for which no negative values may appear. For example, the order number in MetaTrader 5 is a value of the ulong type.

We have already encountered the integer description samples in [Part 1](/en/book/intro). In particular, input parameter GreetingHour of type uint was defined there:

```
input uint GreetingHour = 0;

```

Except for the additional keyword, input, that makes the variable visible in the list of parameters of an MQL program, other components, i.e., type, name, and optional initialization after the '=' sign, are intrinsic to all variables.

Variable description syntax will be considered in detail in the [Variables](/en/book/basis/variables) section. So far, please note the method of recording the constants of integer type. In describing a variable, constants can be specified as a default value (in the example above, it is 0). Moreover, constants can be used in [expressions](/en/book/basis/expressions), for instance, in a formula event.

It should be reminded that constants of any type, inserted in the source code, are named literals (textually: "word-for-word"). Their name derives from the fact that they are introduced into the program "as is" and used immediately at the point of description. Literals, unlike many other elements of the language, particularly variables, have no names and cannot be referred to from other points of the program.

For negative numbers, it is required to provide the minus sign '-' before the number; however, the plus sign '+' can be omitted for positive numbers, i.e., forms +100 and just 100 are identical.

It should be noted that numeric values are usually recorded in the source code within our habitual decimal notation. However, MQL5 allows using the other one, i.e., hexadecimal. It is convenient for processing bit-level information (see [Bitwise operations](/en/book/basis/expressions/operators_bitwise)).

Numbers from 0 through 9 are permitted in all digit order numbers in decimal constants, while for hexadecimal ones, along with digits, Latin symbols from A through F or from a through f (that is, case does not matter) are used additionally. "Hexadecimal digit" A corresponds with number 10 of decimal notation, B — 11, C — 12, etc., up through F equal to 15.

A distinctive feature of a hexadecimal constant is the fact that it begins with prefix 0x or 0X, followed by the significant digit orders of the number. For instance, number 1 is recorded as 0x1 in the hexadecimal system, while 16 as 0x10 (an additional higher order digit is required because 16 is greater than 15, that is, 0xF). Decimal 255 turns into 0xFF.

Let's give some more examples illustrating various situations of using integer types in describing variables (attached in script MQL5/Scripts/MQL5Book/p2/TypeInt.mq5):

```
void OnStart()
{
  int x = -10;          // ok, signed integer x = -10
  uint y = -1;          // ok, but unsigned integer y = 4294967295
  int z = 1.23;         // warning: truncation of constant value, z = 1
  short h = 0x1000;     // ok, h = 4096 in decimal
  long p = 10000000000; // ok
  int w = 10000000000;  // warning, truncation..., w = 1410065408
}

```

Variable x is initialized correctly by the permitted negative value, -10.

Variable y is unsigned. Therefore, an attempt to record a negative value in it leads to an interesting effect. Number -1 has a representation in bits, which is interpreted by the program in accordance with the unsigned type, uint. Therefore, number 4294967295 is obtained (it is actually equal to UINT_MAX).

Variable z is assigned with the floating-point number 1.23 (they will be considered in the next section), and the compiler warns about the truncation of the fractional part. As a result, integer 1 gets into the variable.

Variable h is successfully initialized by a constant in the hexadecimal form (0x1000 = 4096).

The large value 10000000000 is recorded in variables p and w, the former of which is of a long integer type (long) and processed successfully, while the latter one of the normal type (int) and, therefore, calls for the compiler warning. Since the constant exceeds the maximum value for int, compiler truncates the excessive higher order digits (bits) and, in fact, 1410065408 gets into w.

This behavior is one of the potential negative developments of type conversions that may or not may be implied by the programmer. In the latter case, it is fraught with a potential error. Clearly, in this particular example, wrong values were selected intentionally to demonstrate warnings. It is not always that obvious in a real program, which values the program is attempting to save in the integer variable. Therefore, you should look into the compiler warnings very carefully and try to make away with them, having changed the type or explicitly specified the required typecast. This will be considered in the section dealing with [Typecasting](/en/book/basis/conversion).

For integer types, arithmetic, bitwise, and other types of operations are defined (see chapter [Expressions](/en/book/basis/expressions)).
