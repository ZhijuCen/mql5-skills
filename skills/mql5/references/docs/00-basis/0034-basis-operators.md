# Operators

Language operators describe some algorithmic operations that must be executed to accomplish a task. The program body is a sequence of such operators. Operators following one by one are separated by semicolons.

| Operator | Description |
| --- | --- |
| Compound operator {} | One or more operators of any type, enclosed in curly braces {} |
| Expression operator (;) | Any expression that ends with a semicolon (;) |
| return  operator | Terminates the current function and returns control to the calling program |
| if-else  conditional operator | Is used when it's necessary to make a choice |
| ?:  conditional operator | A simple analog of the if-else conditional operator |
| switch  selection operator | Passes control to the operator, which corresponds to the expression value |
| while  loop operator | Performs an operator until the expression checked becomes false. The expression is checked before each iteration |
| for  loop operator | Performs an operator until the expression checked becomes false. The expression is checked before each iteration |
| do-while  loop operator | Performs an operator until the expression checked becomes false. The end condition is checked, after each loop. The loop body is always executed at least once. |
| break  operator | Terminates the execution of the nearest attached external operator switch, while, do-while or for |
| continue  operator | Passes control to the beginning of the nearest external loop operator while, do-while or for |
| @  operator | Implements matrix multiplication according to the rules of linear algebra. It allows multiplying  matrices and vectors , as well as performing scalar multiplication of vectors. |
| new  operator | Creates an object of the appropriate size and returns a descriptor of the created object. |
| delete  operator | Deletes the object created by the new operator |

One operator can occupy one or more lines. Two or more operators can be located in the same line. Operators that control over the execution order (if, if-else, switch, while and for), can be nested into each other.

Example:

```
if(Month() == 12)
  if(Day() == 31) Print("Happy New Year!");

```

See also

[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
