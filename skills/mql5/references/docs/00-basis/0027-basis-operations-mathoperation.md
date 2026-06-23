# Arithmetic Operations

Arithmetic operations include additive and multiplicative operations:

```
Sum of variables                        i = j + 2;
Difference of variables                 i = j - 3;
Changing the sign                       x = - x;
Product of variables                    z = 3 * x;
Division quotient                       i = j / 5;
Remainder of division                   minutes = time % 60;
Adding 1 to the variable value          i++;
Adding 1 to the variable value          ++i;
Subtracting 1 from the variable value   k--;
Subtracting 1 from the variable value   --k;

```

Increment and decrement operations are applied only to variables, they can't be applied to constants. The prefix increment (++i) and decrement (--k) are applied to the variable right before this variable is used in an expression.

Post-increment (i++) and post-decrement (k--) are applied to the variable right after this variable is used in an expression.

Important Notice

```
int i=5;
int k = i++ + ++i;

```

Computational problems may occur while moving the above expression from one programming environment to another one (for example, from Borland C++ to MQL5). In general, the order of computations depends on the compiler implementation. In practice, there are two ways to implement the post-decrement (post-increment):

1. The post-decrement (post-increment) is applied to the variable after calculating the whole expression.
2. The post-decrement (post-increment) is applied to the variable immediately at the operation.

Currently the first way of post-decrement (post-increment) calculation is implemented in MQL5. But even knowing this peculiarity, it is not recommended to experiment with its use.

Examples:

```
int a=3;
a++;            // valid expression
int b=(a++)*3;  // invalid expression

```

See also

[Precedence Rules](/en/docs/basis/operations/rules)
