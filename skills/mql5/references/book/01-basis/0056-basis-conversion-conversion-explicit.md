# Explicit type conversion

For explicit type conversion, MQL5 supports two forms of notation: in the C style and "functional". C-style has the following syntax:

```
target t = (target)s;

```

Where target is the name of the target type. Any expression can be a data source s. If any operations are performed in it, you must enclose the expression in parentheses so that the type conversion applies to the entire expression.

An alternative "functional" syntax looks like this:

```
target t = target(s);

```

Let's look at a couple of examples.

```
double w = 100.0, v = 7.0;
int p = (int)(w / v);      // 14

```

Here, the result of dividing two real numbers is explicitly converted to the type int. Thus, the programmer confirms their intention to discard the fractional part, and the compiler will not issue warnings. It should be noted that MQL5 has a group of functions for rounding real numbers in various ways (see [Math functions](/en/book/common/maths)).

If, on the contrary, you want to perform an operation on integer numbers with a real result, you need to apply type conversion to the operands (in the expression itself):

```
int x = 100, y = 7;
double d = (double)x / y;  // 14.28571428571429

```

Converting one of the operands is enough to automatically convert the rest to the same type.

If necessary, you can perform several type conversion operations sequentially. Because the conversion operation is right-associative, the target types will be applied in order from right to left. In the following example, we convert the quotient to type float (this conversion allows for a more compact, fewer-character representation of the value), and then to string. Without an explicit conversion to string, we would get a compiler warning "implicit number to string conversion".

```
Print("Result:" + (string)(float)(w / v)); // Result:14.28571

```

Don't use explicit type conversion just to avoid a compiler warning. If it has no practical basis, you are masking a potential error in the program.
