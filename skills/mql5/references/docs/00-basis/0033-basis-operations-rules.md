# Precedence Rules

Each group of operations in the table has the same priority. The higher the priority of operations is, the higher it is position of the group in the table. The precedence rules determine the grouping of operations and operands.

Attention: Precedence of operations in the MQL5 language corresponds to the priority adopted in C++, and differs from the priority given in the MQL4 language.

| Operation | Desciption | Execution Order |
| --- | --- | --- |
| () 
 [] 
 . | Function Call 
 Referencing to an array element 
 Referencing to a structure element | From left to right |
| ! 
 ~ 
 – 
 ++ 
 -- 
 (type) 
 sizeof | Logical negation 
 Bitwise negation (complement) 
 Sign changing 
 Increment by one 
 Decrement by one 
 Typecasting 
 Determining size in bytes | Right to left |
| * 
 / 
 % | Multiplication 
 Division 
 Module division | From left to right |
| + 
 – | Addition 
 Subtraction | From left to right |
| << 
 >> | Left shift 
 Right shift | From left to right |
| < 
 <= 
 > 
 >= | Less than 
 Less than or equal 
 Greater than 
 Greater than or equal | From left to right |
| == 
 != | Equal 
 Not equal | From left to right |
| & | Bitwise AND operation | From left to right |
| ^ | Bitwise exclusive OR | From left to right |
| | | Bitwise OR operation | From left to right |
| && | Logical AND operation | From left to right |
| || | Logical OR operation | From left to right |
| ?: | Conditional Operator | Right to left |
| = 
 *= 
 /= 
 %= 
 += 
 -= 
 <<= 
 >>= 
 &= 
 ^= 
 |= | Assignment 
 Multiplication with assignment 
 Division with assignment 
 Module with assignment 
 Addition with assignment 
 Subtraction with assignment 
 Left shift with assignment 
 Right shift with assignment 
 Bitwise AND with assignment 
 Exclusive OR with assignment 
 Bitwise OR with assignment | Right to left |
| , | Comma | From left to right |

To change the operation execution order, parenthesis that are of higher priority are used.
