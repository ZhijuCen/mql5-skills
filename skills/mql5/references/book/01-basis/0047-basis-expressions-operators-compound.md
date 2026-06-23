# Modification operations

Modification that is also called compound assignment allows combining within one operator [arithmetic](/en/book/basis/expressions/operators_arithmetic) or [bitwise](/en/book/basis/expressions/operators_bitwise) operations with normal [assignment](/en/book/basis/expressions/operator_assignment).

| P | Symbols | Description | Example | A |
| --- | --- | --- | --- | --- |
| 14 | += | Addition with assignment | e1 += e2 | R |
| 14 | -= | Subtraction with assignment | e1 -= e2 | R |
| 14 | *= | Multiplication with assignment | e1 *= e2 | R |
| 14 | /= | Division with assignment | e1 /= e2 | R |
| 14 | %= | Division modulo with assignment | e1 %= e2 | R |
| 14 | <<= | Left shift with assignment | e1 <<= e2 | R |
| 14 | >>= | Right shift with assignment | e1 >>= e2 | R |
| 14 | &= | Bitwise AND with assignment | e1 &= e2 | R |
| 14 | |= | Bitwise OR with assignment | e1 |= e2 | R |
| 14 | ^= | Bitwise AND/OR with assignment | e1 ^= e2 | R |

These operators execute the relevant action for operands e1 and e2, whereupon the result is stored in e1.

An expression like e1 @= e2 where @ is any operator from the table is approximately equivalent to e1 = e1 @ e2. The word "approximately" emphasizes the presence of some subtle aspects.

First, if the place of e2 is occupied by an expression with an operator having a lower priority than that of @, e2 is still calculated before that. That is, if the priority is marked with parentheses, we will get e1 = e1 @ (e2).

Second, if there are side modifications of variables in expression e1, they are made only once. The following example demonstrates this.

```
int a[] = {1, 2, 3, 4, 5};
int b[] = {1, 2, 3, 4, 5};
int i = 0, j = 0;
a[++i] *= i + 1;           // a = {1, 4, 3, 4, 5}, i = 1
                           // not equivalent!
b[++j] = b[++j] * (j + 1); // b = {1, 2, 4, 4, 5}, j = 2

```

Here, arrays a and b contain identical elements and are processed using index variables i and j. At the same time, the expression for array a uses operation '*=', while that for array b uses the equivalent. Results are not equal: Both index variables and arrays differ.

Other operators will be useful in problems with bit-level manipulations. Thus, the following expression can be used to set a specific bit into 1:

```
ushort x = 0;
x |= 1 << 10;

```

Here, shift 1 ('0000 0000 0000 0001') is made by 10 bits to the left, which results in obtaining a number with one set 10th bit ('0000 0100 0000 0000'). Bitwise OR operation copies this bit into variable x.

To reset the same bit, we will write:

```
x &= ~(1 << 10);

```

Here, the inversion operation is applied to 1 shifted by 10 bits to the left (which we saw in the preceding expression), which results in all bits changing their value: '1111 1011 1111 1111'. Bitwise AND operation resets the zeroed bits (in this case, one) in variable x, while all other bits in x remain unchanged.
