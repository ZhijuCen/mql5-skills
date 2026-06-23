# Arithmetic type conversions

In arithmetic calculation and comparison expressions, values of different types are often used as operands. To process them correctly, it is necessary to bring the types to a certain "common denominator". The compiler attempts to do this without the programmer's intervention unless the programmer has specified explicit conversion rules (see [Explicit type conversion](/en/book/basis/conversion/conversion_explicit)). In this case, the compiler, whenever possible, tries to preserve the maximum precision when it comes to numbers. In particular, it produces an increase in the capacity of integer numbers and the transition from integer to real numbers (if they are involved).

Integer expansion implies conversion of bool, char, unsigned char, short, unsigned short to int (or unsigned int if int isn't big enough to store specific numbers). Large values can be converted to long and unsigned long.

If the type of the variable is not able to store the result of the type that was obtained when the expression was evaluated, the compiler will issue a warning:

```
double d = 1.0;
int x = 1.0 / 10; // truncation of constant value
int y = d / 10;   // possible loss of data due to type conversion

```

The expression to initialize the variables x and y contains the real number 1.0, so the other operands (constant 10 in this case) are converted to double, and the result of division will also be of type double. However, the type of variables is int, and therefore an implicit conversion to it takes place.

Calculation 1.0 / 10 is done by the compiler during compilation and therefore it gets a constant of type double (0.1). Of course, in practice, it is unlikely that the initializing constant will exceed the size of the receiving variable. Therefore, the compiler warning "truncation of constant value" can be considered exotic. It just shows the problem in the most simplified way.

However, as a result of variable-based calculations, similar data loss can also occur. The second compiler warning we see here ("possible loss of data due to type conversion") occurs much more frequently. Moreover, the loss is possible not only when converting from real type to integer, but also vice versa.

```
double f = LONG_MAX; // truncation of constant value
long m1 = 1000000000;
f = m1 * m1;         // possible loss of data due to type conversion

```

As we know, type double cannot accurately represent large integers (although its range of valid values is much larger than long).

Another warning we might encounter due to type mismatch: "integral constant overflow".

```
long m1 = 1000000000;
long m2 = m1 * m1;                 // ok: m2 = 1000000000000000000
long m3 = 1000000000 * 1000000000; // integral constant overflow
                                   // m3 = -1486618624

```

Integer constants in MQL5 have type int, so the multiplication of million by million is performed taking into account the range of this type, which is equal to INT_MAX (2147483647). The value 1000000000000000000 causes an overflow, and m3 gets the remainder after dividing this value by the range (more on this in the sidebar below).

The fact that the receiving variable m3 has type long does not mean that the values ​​in the expression must be converted to it beforehand. This only happens at the moment of assignment. In order for the multiplication to be performed according to the rules of long, you need to somehow specify the type long directly in the expression itself. This can be done with an explicit conversion or by using variables. In particular, obtaining the same product using a variable m1 of type long (such as m1 * m1) leads to the correct result in m2.

Signed and unsigned integers  

   

Programs are not always written perfectly, with protection from all possible failures. Therefore, sometimes it happens that the integer number obtained during the calculations does not fit into the variable of the selected integer type. Then it gets the remainder of dividing this value by the maximum value (M) that can be written in the corresponding number of bytes (type size), plus 1. So for integer types with sizes from 1 to 4 bytes, M + 1 is, respectively, 256, 65536, 4294967296, and 18446744073709551616.  

   

But there is a nuance for signed types. As we know, for signed numbers, the total range of values ​​is divided approximately equally between positive and negative areas. Therefore, the new "residual" value may in 50% of cases exceed the positive or negative limit. In this case, the number turns into the "opposite": it changes sign and ends up at a distance M from the original one.  

   

It is important to understand that this transformation occurs only due to a different interpretation of the bit state in the internal representation, and the state itself is the same for signed and unsigned numbers.  

   

Let's explain this with an example for the smallest integer types: char and uchar.  

   

Since unsigned char can store values ​​from 0 to 255, 256 maps to 0, -1 maps to 255, 300 maps to 44, and so on. If we try to write 300 into a regular signed char, we also get 44, because 44 is in the range from 0 to 127 (the positive range of char). However, if you set the variables char and uchar to 3000, the picture will be different. The remainder of 3000 divided by 256 is 184. It ends up in uchar unchanged. However, for char, the same combination of bits results in -72. It is easy to check that 184 and -72 differ by 256.

In the following example, it is easy to spot the problem thanks to the compiler warning.

```
char c = 3000;      // truncation of constant value
Print(c);           // -72
uchar uc = 3000;    // truncation of constant value
Print(uc);          // 184

```

However, if you get an extra large number during the calculation, there will be no warning.

```
char c55 = 55;
char sm = c55 * c55;  // ok! 
Print(sm);            // 3025 -> -47
uchar um = c55 * c55; // ok!
Print(um);            // 3025 -> 209

```

A similar effect can occur when signed and unsigned integer numbers of the same size are used in the same expression since the signed operand is converted to unsigned. For example:

```
uint u = 11;
int i = -49;
Print(i + i); // -98
Print(u + i); // 4294967258 = 4294967296 - 38

```

When two negative integers add up, we get the expected result. The second expression maps the sum of -38 to the "opposite" unsigned number 4294967258.

Mixing signed and unsigned types in the same expression is not recommended because of these potential issues.

Besides that, if we subtract something from an unsigned integer, we need to make sure that the result doesn't come out negative. Otherwise, it will be converted to a positive number and can distort the idea of the algorithm, in particular, the idea of the [while](/en/book/basis/statements/statements_while)[ loop](/en/book/basis/statements/statements_while) which checks the variable for the "greater than or equal to zero" condition: since unsigned numbers are always non-negative, we can easily get an infinite loop, i.e. a program hang.
