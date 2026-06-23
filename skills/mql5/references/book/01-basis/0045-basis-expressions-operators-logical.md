# Logical operations

Logical operations perform computations on logical operands and return a result of the same type.

| P | Symbols | Description | Example | A |
| --- | --- | --- | --- | --- |
| 2 | ! | Logical NOT | !e1 | R |
| 11 | && | Logical AND | e1 && e2 | L |
| 12 | || | Logical OR | e1 || e2 | L |

Logical NOT transforms true into false and false into true.

Logical AND is equal to true if both operands are equal to true.

Logical OR is equal to true if at least one operand is equal to true.

Operators AND and OR always compute operands from left to right and, if possible, use the computational shortcut. If the left operand is equal to false, then operator AND skips the second operand, because it does not affect anything – the result is already false. If the left operand is equal to true, then operator OR skips the second operand for the same reason, since the result will, in any case, be equal to true.

This is often used in programs to prevent from errors in the second (and subsequent) operands. For example, we can hedge ourselves against the error of accessing a non-existing array element:

```
index < ArraySize(array) && array[index] != 0

```

Here we use the built-in function ArraySize that returns the array length. Only if index is smaller than the length, the element with this index is read and compared with zero.

Checking by contraries, using '||' is also used, for example:

```
ArraySize(array) == 0 || array[0] == 0

```

The condition is true immediately if the array is null. And only if there are elements, the additional check for the contents will continue.

If the expression consists of multiple operands combined by logical OR, then with the first true (if any) the total result of true will be obtained immediately. However, if operands are combined by logical AND, then with the first false the total result of false will be obtained immediately.

Of course, you can combine different operations within one expression, considering their different priority: Negation is executed first, then the AND-related conditions, and in the end the OR-related conditions. If another sequence is required, it must be explicitly specified using parentheses.

For example, the following expression without parentheses, A && B || C && D, is in fact equivalent to: (A && B) || (C && D). For the logical OR to be executed as the first, it should be enclosed in parentheses: A && (B || C) && D. For more details on using parentheses, see section [Grouping with Parentheses](/en/book/basis/expressions/operators_parentheses).

Simple examples are given in script ExprLogical.mq5 to check logical operations in practice.

```
int x = 3, y = 4, z = 5;
bool expr1 = x == y && z > 0;  // false, x != y, z does not matter
bool expr2 = x != y && z > 0;  // true,  both conditions are complied with
bool expr3 = x == y || z > 0;  // true,  it is sufficient that z > 0
bool expr4 = !x;               // false, x must be 0 to get true
bool expr5 = x > 0 && y > 0 && z > 0; // true, all 3 are complied with
bool expr6 = x < 0 || y > 0 && z > 0; // true, y and z are sufficient
bool expr7 = x < 0 || y < 0 || z > 0; // true, z is sufficient

```

In the string of calculating expr6, the compiler gives the warning: "Check operator precedence for possible error; use parentheses to clarify precedence".

Logical operations '&&' and '||' should not be mixed with bitwise operations '&' and '|' (considered in the [next section](/en/book/basis/expressions/operators_bitwise)).
