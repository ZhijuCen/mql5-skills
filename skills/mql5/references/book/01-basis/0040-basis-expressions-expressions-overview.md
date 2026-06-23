# Basic concepts

Before proceeding to the specific groups of operators, we should introduce some basic concepts that are inherent in all operators and affect their applicability and behavior in a particular context.

First of all, by the quantity of operands required, operators can be unary and binary. As is clear from the names, unary ones process one operand, while binary operators process two. In the case of binary, the operator is always placed between operands. Among unary ones, there are operators that must be put before the operand and those to be placed after it. For example, the unary minus ('-') operator allows reversing the sign of the value:

```
int x = 10;
int y = -x;  // -10

```

At the same time, there is a binary operator for subtraction using the same character, '-'.

```
int z = x - y; // 10 - -10 -> 20

```

Choosing a correct operator (action) by the compiler in a specific context is determined by the context of using it in the expression.

Each operator is assigned priority. It determines the order, in which operators will be computed in complex expressions where there are multiple operators. Higher-priority operators are computed as the first, while the lowest-priority ones as the last. For instance, in the expression 1 + 2 * 3 there are two operations (addition and multiplication) and three operands. Since multiplication has a priority higher than that of addition, the product of 2 * 3 will be found first, and then it will be added to one.

Later we will provide the full table of operations with priorities.

Additionally, each operator is characterized by the associativity. It can be left or right and determines the order, in which the successive operators having the same priority are executed. For example, expression 10 - 7 - 1 can purely theoretically be computed in two ways:

- Subtract 7 from 10 and then subtract 1 from the resulting 3, which gives 2; or
- Subtract 1 from 7, which gives 6, and then subtract 6 from 10, resulting in 4.

In the first case, computations were performed from left to right, which corresponds with the left associativity; since the subtraction operation is left-associative, indeed, the first answer is correct.

The second option of computations corresponds with the right associativity and won't be used.

Let's consider another example where there are priority and associativity involved simultaneously: 11 + 5 * 4 / 2 + 3. Both types of operations, i.e., addition and multiplication, are executed from left to right. If the priorities were not different, we would get 35, although 24 is the correct answer. Changing associativity for the right would give us 14.

To explicitly redefine priorities in expressions, parentheses can be used, for instance: (11 + 5) * 4 / (2 + 3). What is enclosed in parentheses is computed earlier, and the intermediate result is substituted in the expression to be used in other operations. Groups in parentheses can be nested. For more details, please see section [Grouping with Parentheses](/en/book/basis/expressions/operators_parentheses).

A right-associative operator can be exemplified by the unary operator of logic negation, '!'. Essentially, its task is to make true from false, and vice versa. Like with other unary operators, associativity means in this context, what side of the operator the operand must be placed. Symbol '!' is placed before the operand, i.e., the operand is to the right.

```
int x = 10;
int on_off = !!x;  // 1

```

In this case, logic negation is performed twice: first time regarding variable x (right '!') and the second time regarding the result of the preceding negation (left '!'). Such double negation allows transforming any nonzero value into 1 due to converting into bool and back.

The final table of operations will also show associativity.

Finally, the last but not the least fine point in processing expressions is the order of computing the operands. It should be distinguished from the priority that belongs to the operation, not operands. The order of computing the operands of binary operations is not defined explicitly, which gives the compiler space to optimize the code and enhance its efficiency. The compiler only guarantees that operands will be computed before executing the operation.

There is a limited set of operations, for which the operand evaluation order is defined. Particularly, for logic AND ('&&') and OR ('||') it is from left to right, and the right part may be omitted if it does not affect anything due to the value of the left part. But as far as the [ternary conditional operator](/en/book/basis/expressions/operator_conditional) '?:' goes, the order is even more intricate, since either one or another branch will be calculated upon computing the first conditions, depending on its trueness. See further sections for more details.

Operand evaluation order is illustrated by the situation where there are several [function](/en/book/basis/functions) calls in the expression. For instance, let 4 functions be used in the expression:

```
a() + b() * c() - d()

```

Priority and associativity rules will only be used for the intermediate results of calling these functions, while the calls themselves can be generated by the compiler in any order it "considers to be necessary" based on the source code features and compiler settings. For example, functions b and c involved in multiplication may be called in the order of [b(), c()] or, vice versa, [c(), b()]. If the functions during being executed may affect the same data, their state will be ambiguous upon the expression computation.

A similar problem can be seen when working with arrays and increment operators (see [Increment and Decrement](/en/book/basis/expressions/increment_decrement)).

```
int i = 0;
int a[5] = {0, 1, 2, 3, 4};
int w = a[++i] - a[++i];

```

Depending on whether the left or the right difference operand will be computed as the first, we can get -1 (a[1] - a[2]) or +1 (a[2] - a[1]). Since the MQL5 compiler is ever-improving, there is no guarantee that the current result (-1) will be retained in the future.

To avoid potential issues, it is recommended not to use an operand repeatedly, if it has already been modified in the same expression.

In all expressions, there can usually be operands of different types. This leads to the need to cast them to a certain common type, before performing any actions with them. If there are no explicit typecasts, MQL5 performs the implicit conversion where necessary. Besides, conversion rules are different for different type combinations. Explicit and implicit typecasting is discussed in the [relevant section](/en/book/basis/conversion).
