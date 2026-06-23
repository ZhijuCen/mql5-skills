# Grouping with parentheses

In the preceding sections, we have already seen more than a few times that some expressions can cause unexpected results due to the priorities of operations. To explicitly change the computation order, we should use parentheses. Part of the expression enclosed in them gets a higher priority as compared to the environment, without regard to default priorities. Pairs of parentheses can be nested, but it is not recommended to make more than 3-4 nesting levels. It is better to divide the too complex expressions into several simpler ones.

Script ExprParentheses.mq5 shows the evolution of placing parentheses within one expression. The initial intent for it is to set the bit in variable flags using the left-shift operation '<<'. The bit number is taken from variable offset if it is not zero, or otherwise, as 1 (remember that numbering starts with zero). Then the obtained value is multiplied by coefficient. No need to search for any applied sense in this example. However, more sophisticated structures can occur, too.

```
int offset = 8;
int coefficient = 10, flags = 0;
int result1 = coefficient * flags | 1 << offset > 0 ? offset : 1;     // 8
int result2 = coefficient * flags | 1 << (offset > 0 ? offset : 1);   // 256
int result3 = coefficient * (flags | 1 << (offset > 0 ? offset : 1)); // 2560

```

The first version, without parentheses, seems suspicious even to the compiler. It gives a warning that we have already known: "expression not boolean". The matter is that the ternary conditional operator has the lowest priority of all operators here. For this reason, the entire left part before '?' is considered its condition. Inside the condition, calculations are in the following order: Multiplication, bitwise shift, "more than" comparison, and bitwise OR, which results in an integer. Of course, it can be used as true or false, but it is desired to "communicate" such intentions to the compiler using [explicit typecasting](/en/book/basis/conversion/conversion_explicit). If it is absent, the compiler considers the expression suspicious, and not in vain. The first calculation results in 8. It is incorrect.

Let's add parentheses around the ternary operator. The warning of the compiler will disappear. However, the expression is still computed wrongly. Since the priority of multiplication is higher than that of bitwise OR, variables coefficient and flags are multiplied before the bit mask is used, which is obtained by shifting to the left. The result is 256.

Finally, having added another pair of parentheses, we will get the correct result: 2560.
