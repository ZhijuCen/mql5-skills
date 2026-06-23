# Universal formatted data output to a string

When generating a string to display to the user, to save to a file, or to send over the Internet, it may be necessary to include the values of several variables of different types in it. This problem can be solved by explicitly casting all variables to the type (string) and adding the resulting strings, but in this case, the MQL code instruction will be long and difficult to understand. It would probably be more convenient to use the [StringConcatenate](/en/book/common/strings/strings_concatenation) function, but this method does not completely solve the problem.

The fact is that a string usually contains not only variables, but also some text inserts that act as connecting links and provide the correct structure of the overall message. It turns out that pieces of formatting text are mixed with variables. This kind of code is hard to maintain, which goes against one of the well-known principles of programming: the separation of content and presentation.

There is a special solution for this problem: the StringFormat function.

The same scheme applies to another MQL5 API function: [PrintFormat](/en/book/common/output/output_print).

string StringFormat(const string format, ...)

The function converts arbitrary built-in type arguments to a string according to the specified format. The first parameter is the template of the string to be prepared, in which the places for inserting variables are indicated in a special way and the format of their output is determined. These control commands may be interspersed with plain text, which is copied to the output string unchanged. The following function parameters, separated by commas, list all the variables in the order and types that are reserved for them in the template.

![Interaction of the format string and StringFormat arguments](pics/sprintf.png)

Interaction of the format string and StringFormat arguments

Each variable insertion point in a string is marked with a format specifier: the character '%', after which several settings can be specified.

The format string is parsed from left to right. When the first specifier (if any) is encountered, the value of the first parameter after the format string is converted and added to the resulting string according to the specified settings. The second specifier causes the second parameter to be converted and printed, and so on, until the end of the format string. All other characters in the pattern between the specifiers are copied unchanged into the resulting string.

The template may not contain any specifier, that is, it can be a simple string. In this case, you need to pass a dummy argument to the function in addition to the string (the argument will not be placed in the string).

If you want to display the percent sign in the template, then you should write it twice in a row %%. If the % sign is not doubled, then the next few characters following % are always parsed as a specifier.

A mandatory attribute of a specifier is a symbol that indicates the expected type and interpretation of the next function argument. Let's conditionally call this symbol T. Then, in the simplest case, one format specifier looks like %T.

In a generalized form, the specifier can consist of several more fields (optional fields are indicated in square brackets):

%[Z][W][.P][M]T

Each field performs its function and takes one of the allowed values. Next, we will gradually consider all the fields.

Type T

For integers, the following characters can be used as T, with an explanation of how the corresponding numbers are displayed in the string:

- c — Unicode character
- C — ANSI character
- d, i — signed decimal
- o — unsigned octal
- u — unsigned decimal
- x — unsigned hexadecimal (lowercase)
- X — unsigned hexadecimal (capital letters)

Recall that according to the method of internal data storage, integer types also include built-in MQL5 types datetime, color, bool and enumerations.

For real numbers, the following symbols are applicable as T:

- e — scientific format with exponent (lowercase 'e')
- E — scientific format with exponent (capital 'E')
- f — normal format
- g — analog of f or e (the most compact form is chosen)
- G — analog of f or E (the most compact form is chosen)
- a — scientific format with exponent, hexadecimal (lowercase)
- A — scientific format with exponent, hexadecimal (capital letters)

Finally, there is only one version of the T character available for strings: s.

Size of integers M

For integer types, you can additionally explicitly specify the size of the variable in bytes by prefixing T with one of the following characters or combinations of them (we have generalized them under the letter M):

- h — 2 bytes (short, ushort)
- l (lowercase L) — 4 bytes (int, uint)
- I32 (capital i) — 4 bytes (int, uint)
- ll (two lowercase Ls) — 8 bytes (long)
- I64 (capital i) — 8 bytes (long, ulong)

Width W

The W field is a non-negative decimal number that specifies the minimum number of character spaces available for the formatted value. If the value of the variable fits into fewer characters, then the corresponding number of spaces is added to the left or right. The left or right side is selected depending on the alignment (see the flag further '—' in the Z field). If the '0' flag is present, the corresponding number of zeros is added in front of the output value. If the number of characters to be output is greater than the specified width, then the width setting is ignored and the output value is not truncated.

If an asterisk '*' is specified as the width, then the width of the output value should be specified in the list of passed parameters. It should be a value of type int at the position preceding the variable being formatted.

Precision P

The P field also contains a non-negative decimal number and is always preceded by a dot '.'. For integer T, this field specifies the minimum number of significant digits. If the value fits in fewer digits, it is prepended with zeros.

For real numbers, P specifies the number of decimal places (default is 6), except for the g and G specifiers, for which P is the total number of significant digits (mantissa and decimal).

For a string, P specifies the number of characters to display. If the string length exceeds the precision value, then the string will be shown as truncated.

If the asterisk '*' is specified as the precision, it is treated in the same way as for the width but controls the precision.

Fixed width and/or precision, together with the right-alignment, makes it possible to display values in a neat column.

Flags Z

Finally, the Z field describes the flags:

- - (minus) — left alignment within the specified width (in the absence of the flag, right alignment is done);
- + (plus) — unconditional display of a '+' or '-' sign before the value (without this flag, only '-' is displayed for negative values);
- 0 — zeros are added before the output value if it is less than the specified width;
- (space) — a space is placed before the displayed value if it is signed and positive;
- # — controls the display of octal and hexadecimal number prefixes in formats o, x or X (for example, for the format x prefix "0x" is added before the displayed number, for the format X — prefix "0X"), decimal point in real numbers (formats e, E, a or A) with a zero fractional part, and some other nuances.

You can learn more about the possibilities of formatted output to a string in the [documentation](https://www.mql5.com/ru/docs/common/printformat).

The total number of function parameters cannot exceed 64.

If the number of arguments passed to the function is greater than the number of specifiers, then the extra arguments are omitted.

If the number of specifiers in the format string is greater than the arguments, then the system will try to display zeros instead of missing data, but a text warning ("missing string parameter") will be embedded for string specifiers.

If the type of the value does not match the type of the corresponding specifier, the system will try to read the data from the variable in accordance with the format and display the resulting value (it may look strange due to a misinterpretation of the internal bit representation of the real data). In the case of strings, a warning ("non-string passed") may be embedded in the result.

Let's test the function with the script StringFormat.mq5.

First, let's try different options for T and data type specifier.

```
PRT(StringFormat("[Infinity Sign] Unicode (ok): %c; ANSI (overflow): %C", 
   '∞', '∞'));
PRT(StringFormat("short (ok): %hi, short (overflow): %hi", 
   SHORT_MAX, INT_MAX));
PRT(StringFormat("int (ok): %i, int (overflow): %i", 
   INT_MAX, LONG_MAX));
PRT(StringFormat("long (ok): %lli, long (overflow): %i", 
   LONG_MAX, LONG_MAX));
PRT(StringFormat("ulong (ok): %llu, long signed (overflow): %lli", 
   ULONG_MAX, ULONG_MAX));

```

Both correct and incorrect specifiers are represented here (incorrect ones come second in each instruction and are marked with the word "overflow" since the value passed does not fit in the format type).

Here's what happens in the log (the breaks of long lines here and below are made for publication):

```
StringFormat(Plain string,0)='Plain string'
StringFormat([Infinity Sign] Unicode: %c; ANSI: %C,'∞','∞')=
   '[Infinity Sign] Unicode (ok): ∞; ANSI (overflow):  '
StringFormat(short (ok): %hi, short (overflow): %hi,SHORT_MAX,INT_MAX)=
   'short (ok): 32767, short (overflow): -1'
StringFormat(int (ok): %i, int (overflow): %i,INT_MAX,LONG_MAX)=
   'int (ok): 2147483647, int (overflow): -1'
StringFormat(long (ok): %lli, long (overflow): %i,LONG_MAX,LONG_MAX)=
   'long (ok): 9223372036854775807, long (overflow): -1'
StringFormat(ulong (ok): %llu, long signed (overflow): %lli,ULONG_MAX,ULONG_MAX)=
   'ulong (ok): 18446744073709551615, long signed (overflow): -1'

```

All of the following instructions are correct:

```
PRT(StringFormat("ulong (ok): %I64u", ULONG_MAX));
PRT(StringFormat("ulong (HEX): %I64X, ulong (hex): %I64x", 
   1234567890123456, 1234567890123456));
PRT(StringFormat("double PI: %f", M_PI));
PRT(StringFormat("double PI: %e", M_PI));
PRT(StringFormat("double PI: %g", M_PI));
PRT(StringFormat("double PI: %a", M_PI));
PRT(StringFormat("string: %s", "ABCDEFGHIJ"));

```

The result of their work is shown below:

```
StringFormat(ulong (ok): %I64u,ULONG_MAX)=
   'ulong (ok): 18446744073709551615'
StringFormat(ulong (HEX): %I64X, ulong (hex): %I64x,1234567890123456,1234567890123456)=
   'ulong (HEX): 462D53C8ABAC0, ulong (hex): 462d53c8abac0'
StringFormat(double PI: %f,M_PI)='double PI: 3.141593'
StringFormat(double PI: %e,M_PI)='double PI: 3.141593e+00'
StringFormat(double PI: %g,M_PI)='double PI: 3.14159'
StringFormat(double PI: %a,M_PI)='double PI: 0x1.921fb54442d18p+1'
StringFormat(string: %s,ABCDEFGHIJ)='string: ABCDEFGHIJ'

```

Now let's look at the various modifiers.

With right alignment (by default) and a fixed field width (number of characters), we can use different options for padding the resulting string on the left: with a space or zeros. In addition, for any alignment, you can enable or disable the explicit indication of the sign of the value (so that not only minus is displayed for negative, but also plus for positive).

```
PRT(StringFormat("space padding: %10i", SHORT_MAX));
PRT(StringFormat("0-padding: %010i", SHORT_MAX));
PRT(StringFormat("with sign: %+10i", SHORT_MAX));
PRT(StringFormat("precision: %.10i", SHORT_MAX));

```

We get the following in the log:

```
StringFormat(space padding: %10i,SHORT_MAX)='space padding:      32767'
StringFormat(0-padding: %010i,SHORT_MAX)='0-padding: 0000032767'
StringFormat(with sign: %+10i,SHORT_MAX)='with sign:     +32767'
StringFormat(precision: %.10i,SHORT_MAX)='precision: 0000032767'

```

To align to the left, you must use the '-' (minus) flag, the addition of the string to the specified width occurs on the right:

```
PRT(StringFormat("no sign (default): %-10i", SHORT_MAX));
PRT(StringFormat("with sign: %+-10i", SHORT_MAX));

```

Result:

```
StringFormat(no sign (default): %-10i,SHORT_MAX)='no sign (default): 32767     '
StringFormat(with sign: %+-10i,SHORT_MAX)='with sign: +32767    '

```

If necessary, we can show or hide the sign of the value (by default, only minus is displayed for negative values), add a space for positive values, and thus ensure the same formatting when you need to display variables in a column:

```
PRT(StringFormat("default: %i", SHORT_MAX));  // standard
PRT(StringFormat("default: %i", SHORT_MIN));
PRT(StringFormat("space  : % i", SHORT_MAX)); // extra space for positive
PRT(StringFormat("space  : % i", SHORT_MIN));
PRT(StringFormat("sign   : %+i", SHORT_MAX)); // force sign output
PRT(StringFormat("sign   : %+i", SHORT_MIN));

```

Here's what it looks like in the log:

```
StringFormat(default: %i,SHORT_MAX)='default: 32767'
StringFormat(default: %i,SHORT_MIN)='default: -32768'
StringFormat(space  : % i,SHORT_MAX)='space  :  32767'
StringFormat(space  : % i,SHORT_MIN)='space  : -32768'
StringFormat(sign   : %+i,SHORT_MAX)='sign   : +32767'
StringFormat(sign   : %+i,SHORT_MIN)='sign   : -32768'

```

Now let's compare how width and precision affect real numbers.

```
PRT(StringFormat("double PI: %15.10f", M_PI));
PRT(StringFormat("double PI: %15.10e", M_PI));
PRT(StringFormat("double PI: %15.10g", M_PI));
PRT(StringFormat("double PI: %15.10a", M_PI));
   
// default precision = 6
PRT(StringFormat("double PI: %15f", M_PI));
PRT(StringFormat("double PI: %15e", M_PI));
PRT(StringFormat("double PI: %15g", M_PI));
PRT(StringFormat("double PI: %15a", M_PI));

```

Result:

```
StringFormat(double PI: %15.10f,M_PI)='double PI:    3.1415926536'
StringFormat(double PI: %15.10e,M_PI)='double PI: 3.1415926536e+00'
StringFormat(double PI: %15.10g,M_PI)='double PI:     3.141592654'
StringFormat(double PI: %15.10a,M_PI)='double PI: 0x1.921fb54443p+1'
StringFormat(double PI: %15f,M_PI)='double PI:        3.141593'
StringFormat(double PI: %15e,M_PI)='double PI:    3.141593e+00'
StringFormat(double PI: %15g,M_PI)='double PI:         3.14159'
StringFormat(double PI: %15a,M_PI)='double PI: 0x1.921fb54442d18p+1'

```

In the explicit width is not specified, the values are output without padding with spaces.

```
PRT(StringFormat("double PI: %.10f", M_PI));
PRT(StringFormat("double PI: %.10e", M_PI));
PRT(StringFormat("double PI: %.10g", M_PI));
PRT(StringFormat("double PI: %.10a", M_PI));

```

Result:

```
StringFormat(double PI: %.10f,M_PI)='double PI: 3.1415926536'
StringFormat(double PI: %.10e,M_PI)='double PI: 3.1415926536e+00'
StringFormat(double PI: %.10g,M_PI)='double PI: 3.141592654'
StringFormat(double PI: %.10a,M_PI)='double PI: 0x1.921fb54443p+1'

```

Setting the width and precision of values using the sign '*' and based on additional function arguments is performed as follows:

```
PRT(StringFormat("double PI: %*.*f", 12, 5, M_PI));
PRT(StringFormat("string: %*s", 15, "ABCDEFGHIJ"));
PRT(StringFormat("string: %-*s", 15, "ABCDEFGHIJ"));

```

Please note that 1 or 2 integer type values are passed before the output value, according to the number of asterisks '*' in the specifier: you can control the precision and the width separately or both together.

```
StringFormat(double PI: %*.*f,12,5,M_PI)='double PI:      3.14159'
StringFormat(string: %*s,15,ABCDEFGHIJ)='string:      ABCDEFGHIJ'
StringFormat(string: %-*s,15,ABCDEFGHIJ)='string: ABCDEFGHIJ     '

```

Finally, let's look at a few common formatting errors.

```
PRT(StringFormat("string: %s %d %f %s", "ABCDEFGHIJ"));
PRT(StringFormat("string vs int: %d", "ABCDEFGHIJ"));
PRT(StringFormat("double vs int: %d", M_PI));
PRT(StringFormat("string vs double: %s", M_PI));

```

The first instruction has more specifiers than arguments. In other cases, the types of specifiers and passed values do not match. As a result, we get the following output:

```
StringFormat(string: %s %d %f %s,ABCDEFGHIJ)=
   'string: ABCDEFGHIJ 0 0.000000 (missed string parameter)'
StringFormat(string vs int: %d,ABCDEFGHIJ)='string vs int: 0'
StringFormat(double vs int: %d,M_PI)='double vs int: 1413754136'
StringFormat(string vs double: %s,M_PI)=
   'string vs double: (non-string passed)'

```

Having a single format string in every StringFormat function call allows you to use it, in particular, to translate the external interface of programs and messages into different languages: simply download and substitute into StringFormat various format strings (prepared in advance) depending on user preferences or terminal settings.
