# Priorities of operations

Here is the full table of all operations in the order of their priorities.

| P | Symbols | Description | Example | A |
| --- | --- | --- | --- | --- |
| 0 | :: | Scope resolution | n1 :: n2 | L |
| 1 | () | Grouping | (e1) | L |
| 1 | [] | Index | [e1] | L |
| 1 | . | Dereferencing | n1.n2 | L |
| 1 | ++ | Postfix increment | e1++ | L |
| 1 | -- | Postfix decrement | e1-- | L |
| 2 | ! | Logical NOT | !e1 | R |
| 2 | ~ | Bitwise complement (inversion) | ~e1 | R |
| 2 | + | Unary plus | +e1 | R |
| 2 | - | Unary minus | -e1 | R |
| 2 | ++ | Prefix increment | ++e1 | R |
| 2 | -- | Prefix decrement | --e1 | R |
| 2 | (type) | Typecasting | (n1) | R |
| 2 | & | Taking the address | &n1 | R |
| 3 | * | Multiplication | e1 * e2 | L |
| 3 | / | Division | e1 / e2 | L |
| 3 | % | Division modulo | e1 % e2 | L |
| 4 | + | Addition | e1 + e2 | L |
| 4 | - | Subtraction | e1 - e2 | L |
| 5 | << | Shift to the left | e1 << e2 | L |
| 5 | >> | Shift to the right | e1 >> e2 | L |
| 6 | < | Less | e1 < e2 | L |
| 6 | > | Greater | e1 > e2 | L |
| 6 | <= | Less than or equal | e1 <= e2 | L |
| 6 | >= | Greater than or equal | e1 >= e2 | L |
| 7 | == | Equal | e1 == e2 | L |
| 7 | != | Not equal | e1 != e2 | L |
| 8 | & | Bitwise AND | e1 & e2 | L |
| 9 | ^ | Bitwise exclusive OR | e1 ^ e2 | L |
| 10 | | | Bitwise OR | e1 | e2 | L |
| 11 | && | Logical AND | e1 && e2 | L |
| 12 | || | Logical OR | e1 || e2 | L |
| 13 | ?: | Conditional ternary | c1 ? e1 : e2 | R |
| 14 | = | Assignment | e1 = e2 | R |
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
| 15 | , | Comma | e1 , e2 | L |

As we have seen, square brackets are used to specify the indices of array elements and, therefore, have one of the highest priorities.

Along with operators that have been considered earlier, there are some still unknown ones here.

We will learn the [scope resolution](/en/book/oop/classes_and_interfaces/classes_namespace_context) operator '::' within object-oriented programming (OOP). We will also need the dereferencing operator '.' at the same time. Identifiers of types (classes) and their properties, not expressions, act as their operands.

Address-taking operator '&' is intended to pass the [function parameters by referencing](/en/book/basis/functions/functions_ref_value) and to obtain the [object addresses](/en/book/oop/classes_and_interfaces/classes_pointers) in OOP. In both cases, the operator is applied to a variable (LValue).

Explicit typecasting operations will be considered in the [next chapter](/en/book/basis/conversion/conversion_explicit).
