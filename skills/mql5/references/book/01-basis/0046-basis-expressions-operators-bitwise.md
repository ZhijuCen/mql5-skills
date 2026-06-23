# Bitwise operations

Sometimes you may need to process numbers at the bit level. For this purpose, there is a group of bitwise operations applicable to integer types.

All symbols and descriptions of bitwise operators are provided with their associativity and in order of their priority in the table below.

| P | Symbols | Description | Example | A |
| --- | --- | --- | --- | --- |
| 2 | ~ | Bitwise complement (inversion) | ~e1 | R |
| 5 | << | Shift to the left | e1 << e2 | L |
| 5 | >> | Shift to the right | e1 >> e2 | L |
| 8 | & | Bitwise AND | e1 & e2 | L |
| 9 | ^ | Bitwise exclusive OR | e1 ^ e2 | L |
| 10 | | | Bitwise OR | e1 | e2 | L |

Of the entire group, only the bitwise complement operation '~' is unary, while all others are binary.

In all cases, if the operand size is less than int/uint, it is preliminarily extended to int/uint by adding 0 bits into higher order. Based on the operand type being signed/unsigned, a high-order bit may affect the sign.

Standard Windows application, Calculator, may help understand the representation of numbers at the bit level. If you select the Programmer operation mode in the View menu, the groups of toggle buttons will appear in the program to select representing the number in a hexadecimal (Hex), decimal (Dec), octal (Oct), or binary (Bin) form. It is the latter one that shows bits. Moreover, you can select the number size: 1, 2, 4, and 8 bytes. The buttons allow executing all the operations considered: Not ('~'), And ('&'), Or ('|'), Xor ('^'), Lsh ('<<'), and Rsh ('>>').  

   

Since the Calculator uses signed numbers, negative values may appear when toggling to the decimal mode (remember that the high-order bit is interpreted as a sign). For convenient analysis, it is reasonable to exclude the minus that appears, for which purpose it is necessary to select the size in bytes one grade higher. For example, to check the values within the range up to 255 (uchar, unsigned one-byte integer), you should select 2 bytes (otherwise, only decimal values through 127 will be positive, while the others will be displayed in the negative region).

Bitwise complement creates a value, in which the 0-bit is in the place of all 1-bits, while 1-bit is in the place of 0-bits. For example, the negation of a byte with all zero bits gives a byte with all 1 bits. Number 50 appears in the bitwise format as '00110010' (byte). Its inversion gives '11001101'.

Unity represented hexadecimally is 0x0001 (for short). Inversion of these bits gives 0xFFFE (see script ExprBitwise.mq5).

```
short v = ~1;  // 0xfffe = -2
ushort w = ~1; // 0xfffe = 65534

```

Bitwise AND checks each bit in both operands and in the positions where two set bits (1) are found, stores the 1-bit into the result. In all other cases (where there is only a set bit in one operand or they are reset in both places), the 0-bit is written in the result.

Bitwise OR writes 1-bits into the result if they are on the positions where there is a set bit in at least one of two operands.

Bitwise exclusive OR writes in the result the 1-bits on the positions where there is a set bit in either the first or second operand, but not in both at the same time. The binary representation of two numbers, X and Y, and the results of bitwise operations with them are shown below.

```
X       10011010   154
Y       00110111    55
 
X & Y   00010010    18
X | Y   10111111   191
X ^ Y   10101101   173

```

When writing complex expressions from several different operators, use grouping with parentheses in order not to become confused with priorities.

Shift operations move bits to the left ('<<') or right ('>>') by the quantity of bits, defined in the second operand that must be a non-negative integer. As a result, left (for '<<') or right (for '>>') bits are dropped, since they go beyond the memory cell boundaries. With the left shift, the relevant number of 0 bits are added on the right. With the right shift, either 0 bits are added on the left (if the operand is unsigned) or the sign bit is reproduced (if the operand is signed). In the latter case, 0 bits are added on the left for positive numbers and 1 bits for negative ones; i.e., the sign retains.

```
short q = v << 5;  // 0xffc0 = -64
ushort p = w << 5; // 0xffc0 = 65472
short r = q >> 5;  // 0xfffe = -2
ushort s = p >> 5; // 0x07fe = 2046

```

In the example above, the initial left shift "destroyed" the high-order bits of variable p, while the subsequent right shift by the same quantity of bits filled them with zeros, which led to decreasing the value from 0xffc0 to 0x07fe.

Shift size (quantity of bits) must be less than that of the operand type (considering its potential extension). Otherwise, all initial bits will get lost.

Shifting by 0 bits leaves the number unchanged.

Bitwise operations '&' and '|' should not be mixed with logical operations '&&' and '||' (considered in the [preceding section](/en/book/basis/expressions/operators_logical)).
