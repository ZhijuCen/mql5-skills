# Assignment Operations

The value of the expression that includes the given operation is the value of the left operand after assignment:

```
Assigning the value of x to the y variable                              y = x;

```

The following operations unite arithmetic or bitwise operations with operation of assignment:

```
Adding x to the y variable                                             y += x;
Subtracting x from the y variable                                      y -= x;
Multiplying the y variable by x                                        y *= x;
Dividing the y variable by x                                           y /= x;
Reminder of division of the y variable by x                            y %= x;
Shift of the binary representation of y to the right by x bits        y >>= x;
Shift of the binary representation of y to the left by x bits         y <<= x;
AND bitwise operation of binary representations of y and x             y &= x;
OR bitwise operation of binary representations of y and x              y |= x;
Excluding OR bitwise operation of binary representations of y and x    y ^= x;

```

Bitwise operations can be applied to integers only. When performing the operation of the logical shift of the y representation to the right/left by x bits, the 5 smallest binary digits of the x value are used, the highest ones are dropped, i.e. the shift is made to 0-31 bits.

By %= operation (y value by module of x), the result sign is equal to the sign of divided number.

The assignment operator can be used several times in an expression . In this case the processing of the expression is performed from left to right:

```
 y=x=3;

```

First, the variable x will be assigned the value 3, then the y variable will be assigned the value of x, i.e. also 3.

See also

[Precedence Rules](/en/docs/basis/operations/rules)
