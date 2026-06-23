# Increment and decrement

Increment and decrement operators allow writing the increase or decrease of an operand by 1 in a simplified manner. They most frequently occur inside [loops](/en/book/basis/statements/statements_for) to modify indexes when accessing to arrays or other objects supporting enumeration.

The increment is denoted by two consecutive pluses: '++'. Decrement is denoted by two consecutive minuses: '--'.

There are two types of such operators: Prefix and postfix.

Prefix operators, as the name implies, are written before operand (++x, --x). They change the operand value, and this new value is involved in the further calculations of the expression.

Postfix operators are written after operand (x++, x--). They substitute the copy of the current operand value in the expression and then change its value (the new value does not get into the expression). Simple examples are given in the script ExprIncDec.mq5.

```
int i = 0, j;
j = ++i;       // j = 1, i = 1
j = i++;       // j = 1, i = 2

```

Postfix form may be useful for more compact writing of expressions combining a reference to the preceding value of the operand and its side modification (two separate statements would be required to make an alternative record of the same). In all other cases, it is recommended to use the prefix form (it does not create a temporary copy of the "old" value).

In the following example, the sign is reversed in the array elements consecutively, until the zeroth element is found. Moving through the array indices is ensured by postfix increment k++ inside [the loop ](/en/book/basis/statements/statements_while)[while](/en/book/basis/statements/statements_while). Due to postfix, expression a[k++] = -a[k] first updates the kth element and then increases k by 1. Then the assignment result is checked for not being equal to zero (!= 0, see [the following section](/en/book/basis/expressions/operators_relational)).

```
int k = 0;
int a[] = {1, 2, 3, 0, 5};
while((a[k++] = -a[k]) != 0){}
// a[] = {-1, -2, -3, 0, 5};

```

The table below shows the increment and decrement operators in order of priority:

| P | Symbols | Description | Example | A |
| --- | --- | --- | --- | --- |
| 1 | ++ | Postfix increment | e1++ | L |
| 1 | -- | Postfix decrement | e1-- | L |
| 2 | ++ | Prefix increment | ++e1 | R |
| 2 | -- | Prefix decrement | --e1 | R |

All increment and decrement operations have a priority higher than arithmetic operations. Prefixes are of a lower priority than postfixes. In the following example, the "old" value of x is summed up with the value of y, upon which x is incremented. If the prefix priority were higher, the increment of y would be performed, upon which the new value, 6, would be summed up with x, and we would get z = 6, x = 0 (previous).

```
int x = 0, y = 5;
int z = x+++y; // "x++ + y" : z = 5, x = 1

```
