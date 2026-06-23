# Arithmetic operations

Arithmetic operations include 5 binary ones, i.e., addition, subtraction, multiplication, division, and division modulo, and 2 unary ones, i.e., plus and minus. Symbols used for each of those operations are given in the table below.

In the column containing examples, e1 and e2 are arbitrary subexpressions. Associativity is marked with 'L' (left to right) and 'R' (right to left). The number in the first column can be considered as precedence of executing the operations.

| P | Symbols | Description | Example | A |
| --- | --- | --- | --- | --- |
| 2 | + | Unary plus | +e1 | R |
| 2 | - | Unary minus | -e1 | R |
| 3 | * | Multiplication | e1 * e2 | L |
| 3 | / | Division | e1 / e2 | L |
| 3 | % | Division modulo | e1 % e2 | L |
| 4 | + | Addition | e1 + e2 | L |
| 4 | - | Subtraction | e1 - e2 | L |

Order in the table corresponds with decreasing the priorities: Unary plus and minus are calculated before multiplication and division, while the latter ones, in turn, before addition and subtraction.

```
double a = 3 + 4 * 5; // a = 23

```

In fact, unary plus does not have any effect in calculations, but can be used for a better visualization of the expression. Unary minus reverses the sign of its operand.

Arithmetic operations are used for numeric types or those that can be cast to them. The calculation result is an RValue. In computation, the storage locations of integer operands are often extended up to the "largest" of the integers used or to int (if all integer types were of a smaller size), as well as cast to a common type. More details can be found in the section on [Typecasting](/en/book/basis/conversion).

```
bool b1 = true;
bool b2 = -b1;

```

In this example, variable b1 "expands" to the int type with value 1. Sign reversing gives -1, which in the reverse typecasting to bool gives true (because -1 is not zero). Using logic type in arithmetic computations is not welcome.

Dividing integers gives an integer, that is, the fractional part, if any, is omitted. It can be checked using the script ExprArithmetic.mq5.

```
int a = 24 / 7;      // ok: a = 3
int b = 24 / 8;      // ok: b = 3
double c = 24 / 7;   // ok: c = 3 (!)

```

Although variable c is described as double, there are integers in the expression to initialize it; therefore, the division performed is an integer. To perform a division with a fractional part, at least one operand must be of real type (the second one will also be cast to it).

```
double d = 24.0 / 7; // ok: d = 3.4285714285714284

```

Operator '%' calculates the remainder of integer division (it is only applicable to two operands of integer type).

```
int x = 11 % 5;   // ok: x = 1
int y = 11 % 5.0; // no real number can be used
                  // error: '%' - illegal operation use

```

Where operands have different signs, operators '*' and '/' give a negative number. The following rules apply to operator '%':

- if the divisor of operator '%' is negative, the sign "escapes"; and
- if the dividend of operator '%' is negative, the result is negative;

This is easy to check using the alternative calculation of division modulo: m % n = m - m / n * n. It should be kept in mind that division m / n for integers will be rounded; therefore, m / n * n is not equal to m, in the general case.

In section [Characteristics of Arrays](/en/book/basis/arrays/arrays_overview), we delved into the idea that a multidimensional array could be represented by a one-dimensional one due to recalculating the indices of their elements. We also provided the formula to obtain an index through in a one-dimensional array by the coordinates (column number X and row number Y at the string length of N) of the two-dimensional array.

```
index = Y * N + X

```

Operation '%' allows us to perform a more convenient backward calculation, i.e., find X and Y by the index-through:

```
Y = index / N
X = index % N

```

If an unpresentable result NaN (Not A Number, such as infinity, square root of a negative number, etc.) was obtained at some stage during calculating the expression, all subsequent operations with it will also produce a NaN. It can be distinguished from a normal number using the MathIsValidNumber function (see [Mathematical Functions](/en/book/common/maths)).

```
double z = DBL_MAX / DBL_MIN - 1; // inf: Not A Number

```

Here, it is subtracted from the NaN (obtained from division) and gives the NaN again.

Addition operation is defined for strings and performs the concatenation, i.e., combining them.

```
string s = "Hello, " + "world!"; // "Hello, World!"

```

Other operations are prohibited for strings.
