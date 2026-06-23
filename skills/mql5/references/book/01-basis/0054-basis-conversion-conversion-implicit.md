# Implicit type conversion

Type conversion occurs automatically if one type is used at some point in the source code, but another is expected, and there are conversion rules between them. Such conversion is called an implicit type conversion and may not always correspond to the programmer's intent. In addition, some conversion operations have side effects, and the compiler, not knowing whether their use is intentional, highlights the corresponding lines of code with warnings. To solve these problems, there is an explicit type conversion syntax (see [Explicit type casting](/en/book/basis/conversion/conversion_explicit)).

We have already seen several rules for implicit type conversion while studying types and variables.

Specifically, if a value of type other than boolean is assigned to a bool variable, then the value 0 is regarded as false, and all the rest as true. In the more general case, all expressions that assume the presence of logical conditions are converted to type bool. For example, the first operand of a ternary conditional operator is always converted into a bool.

But if a value of type bool is assigned to a numeric type, then true becomes 1, and false becomes 0.

When a real number is assigned to an integer type variable, the fractional part is discarded (the compiler issues a warning). When an integer, on the other hand, is assigned to a variable of real type, precision can be lost (the compiler also issues a warning). We have already talked about this in the sections on [Integer numbers](/en/book/basis/builtin_types/integer_numbers) and [Real numbers](/en/book/basis/builtin_types/float_numbers).

If we have integer and floating point numbers, everything is converted to floating point numbers of the maximum size used (usually double, unless you explicitly specify float or the numeric literal has a suffix 'f', for example1234.56789f).

For integers of different sizes, there are also conversion rules: they expand if necessary, which means that they increase to the size of the largest integer type used in the expression (see [Arithmetic type conversions](/en/book/basis/conversion/conversion_arithmetic)).

In addition to expressions, we often need to implicitly convert types during initialization and assignment, when the types to the right and left of the '=' sign do not match. The same conversion rules apply when passing values through function parameters and returning results from functions (for further details please see the [Functions](/en/book/basis/functions) section).

Considering the above, a large number of conversions can be performed in one line of code. If this causes compiler warnings, it's a good idea to make sure the conversion is intentional and eliminate warnings by inserting an explicit type conversion.

```
short s = 10;
long n = 10;
int p = s * n + 1.0;

```

In this example, when performing a multiplication, the type of the variable s is extended to the type of the second operand long and an intermediate result of type long is obtained. Because the constant 1.0 is of type double, the result of the product is converted to double before addition. The overall result is also of type double; however, the variable p is of type int and therefore an implicit conversion from double to int is performed.

The special types datetime and color are processed according to the rules of integers with lengths of 8 and 4 bytes, respectively. But for date and time, there is a stricter limit on the maximum value - 32535244799, which corresponds to D'3000.12.31 23:59:59'.

Most types can be implicitly converted to and from strings, but the results are not always adequate, so the compiler issues warnings "implicit conversion from 'number' to 'string'" and "implicit conversion from 'string' to 'number'" so that the programmer can check them. For example, converting a string to an integer allows the string to contain only digits and '+'/'-' characters at the beginning. Converting from a string to a real allows, in addition to numbers, the presence of a dot '.' and notation with "exponent" ('e' or 'E', e.g. +1.2345e-1). If an unsupported character (for example, a letter) is encountered in the string, the rest of the string is discarded in full.

For example, the string date and time ("2021.12.12 00:00") cannot be assigned without losses to a variable of type datetime because datetime is an integer (number of seconds). In this case, reading the number from the string will end when the first point is reached, i.e. the number will get the value 2021. This number of seconds corresponds to the 34th minute of the year 1970.

There are special functions for such conversions (see section [Data Transformation](/en/book/common/conversions/conversions_numbers)).

The only direction of implicit and explicit type conversion that is forbidden is from string to bool. The compiler in such cases shows the error message "cannot implicitly convert type 'string' to 'bool'".

Examples from this chapter are provided in TypeConversion.mq5.
