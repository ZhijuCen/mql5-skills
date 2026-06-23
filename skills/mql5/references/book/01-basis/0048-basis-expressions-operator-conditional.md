# Conditional ternary operator

Conditional ternary operator allows describing in a single expression two calculation options, based on a certain condition. The operator syntax is as follows:

```
condition ? expression_true : expression_false

```

The logical condition must be specified in the first operand 'condition'. This can be an arbitrary combination of [comparison operations](/en/book/basis/expressions/operators_relational) and [logical operations](/en/book/basis/expressions/operators_logical). Both branches must be present.

If the condition is true, expression expression_true will be computed, while if it is false, the expression_false will be computed.

This operator guarantees that only one of the expressions expression_true and expression_false will be executed.

Types of the two expressions must be identical, otherwise, there will be an attempt to [implicitly typecast](/en/book/basis/conversion/conversion_implicit) them.

Please note that the result of processing expressions in MQL5 always represents an RValue (in C++, if only LValues are in expressions, then the result of the operator will also be LValue). Thus, the following code is compiled well in C++, but gives an error in MQL5:

```
int x1, y1; ++(x1 > y1 ? x1 : y1); // '++' - l-value required

```

Conditional operators can be nested, that is, it is permitted to use another conditional operator as a condition or either branch (expression_true or expression_false). At the same time, it cannot be always clear what the conditions relate to (if parentheses are not used to explicitly denote grouping). Let's consider examples from ExprConditional.mq5.

```
int x = 1, y = 2, z = 3, p = 4, q = 5, f = 6, h = 7;
int r0 = x > y ? z : p != 0 && q != 0 ? f / (p + q) : h; // 0 = f / (p + q)

```

In this case, the first logical condition represents comparison x > y. If it is true, the branch with variable z is executed. If it is false, the additional logical condition p != 0 && q != 0 is checked, with two expression options, as well.

Below are some more operators, in which logical conditions are written uppercase, while computation options are lowercase. For simplicity, they all are made variables (from the example above). In reality, each of the three components may be a richer expression.

For each string, you can track how the result is obtained, which has been shown in the comment.

```
bool A = false, B = false, C = true;
int r1 = A ? x : C ? p : q;                              // 4
int r2 = A ? B ? x : y : z;                              // 3
int r3 = A ? B ? C ? p : q : y : z;                      // 3
int r4 = A ? B ? x : y : C ? p : q;                      // 4
int r5 = A ? f : h ? B ? x : y : C ? p : q;              // 2

```

Since the operator is right-associative, the compound expression is analyzed from right to left, that is, the rightmost structure with three operands combined by '?' and ':' becomes the operand of the external condition written to the left. Then, considering this substitution, the expression is analyzed from right to left again, and so on, until the final complete upper-level structure '?:' is obtained.

Therefore, the expressions above are grouped as follows (parentheses denote the implicit interpretation of the compiler; but such parentheses could be added into expressions to visualize the source code, which approach is actually recommended).

```
int r0 = x > y ? z : ((p != 0 && q != 0) ? f / (p + q) : h);
int r1 = A ? x : (C ? p : q); 
int r2 = A ? (B ? x : y) : z; 
int r3 = A ? (B ? (C ? p : q) : y) : z; 
int r4 = A ? (B ? x : y) : (C ? p : q); 
int r5 = (A ? f : h) ? (B ? x : y) : (C ? p : q); 

```

For variable r5, the first condition A ? f : h computes the logical condition for the subsequent expression and therefore, is transformed into bool. Since A is equal to false, the value is taken from variable h. It is not equal to 0; therefore, the first condition is considered true. This results in the actuating branch (B ? x : y), from which the value of variable y is returned, since B is equal to false.

There must be all 3 components (a condition and 2 alternatives) in the operator. Otherwise, the compiler will generate the error "unexpected token":

```
// ';' - unexpected token
// ';' - ':' colon sign expected
int r6 = A ? B ? x : y; // lack of alternative

```

In the compiler language, a token is an indivisible fragment of the source code, having its independent meaning or purpose, such as type, identifier, punctuation character, etc. The entire source code is divided by the compiler into a sequence of tokens. Signs of the operators considered are tokens, too. In the code above, there are two symbols '?', and there must be two symbols ':' matching with them, but it is the only one. Therefore, the compiler "says" that the statement end symbol ';' is premature and "inquires" what exactly is deficient: "colon sign expected".

Since the conditional operator has a very low priority (13 in the full table, see [Priorities of Operations](/en/book/basis/expressions/operators_precedence)), it is recommended to enclose it in parentheses. This makes it easier to avoid situations where the operands of a conditional operator could be "caught" by the neighboring operations having higher priorities. Fir instance, if we need to calculate the value of a certain variable w via the sum of two ternary operators, a straightforward approach might appear as follows:

```
int w = A ? f : h + B ? x : y;                           // 1

```

This will work differently than we thought. Due to the higher priority, the sum h + B is considered as a single expression. Considering its parsing from right to left, this sum appears as a condition and is cast to the bool type, which is even warned by the compiler as "expression not boolean". Compiler interpretation can even be visualized by parentheses:

```
int w = A ? f : ((h + B) ? x : y);                       // 1

```

To solve the problem, we should place parentheses in our own way.

```
int v = (A ? f : h) + (B ? x : y);                       // 9

```

Deep nesting of conditional operators impacts adversely on the code understandability. Nesting levels exceeding two or three should be avoided.
