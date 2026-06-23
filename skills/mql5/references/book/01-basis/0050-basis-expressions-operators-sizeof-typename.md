# Special operators sizeof and typename

sizeof

The sizeof operator returns the size of its operand in bytes. Operator syntax: sizeof(x), where x can be a type or an expression. The expression is not computed in this case, since operator sizeof is executed at the compilation stage and, in fact, a constant is substituted in its place in the expression.

For fixed-size arrays, the operator returns the total amount of the allocated memory, that is, the multiplication of the number of elements in all dimensions by the type size in bytes. For dynamic arrays, it returns the size of an internal structure storing the array properties.

Let's give some examples with explanations (ExprSpecial.mq5).

```
double array[2][2];
double dynamic1[][1];
double dynamic2[][2];
Print(sizeof(double));                           // 8
Print(sizeof(string));                           // 12
Print(sizeof("This string is 29 bytes long!"));  // 12
Print(sizeof(array));                            // 32
Print(sizeof(array) / sizeof(double));           // 4 (quantity of elements)
Print(sizeof(dynamic1));                         // 52
Print(sizeof(dynamic2));                         // 52

```

The result to be printed in the log is marked in the comments.

Type double takes up 8 bytes. The size of the string type is 12. These 12 bytes store the service information we mentioned in the section dealing with type [string](/en/book/basis/builtin_types/strings). This memory is allocated for any string (even uninitialized). Please note that a string containing a 29-character text is also sized 12. This is because both an empty string and a string with some contents have an internal structure intended for storing a reference to memory. To obtain the text length, we should use the [StringLen](/en/book/common/strings/strings_init) function.

Fixed-size array size is really computed as the multiplication of the number of elements (2*2=4) by the double type size (8), a total of 32. As a consequence, an expression like sizeof(array) / sizeof(double) allows finding out the entity of elements in it.

For dynamic arrays, the internal structure size is 52 bytes. Differences in the descriptions of arrays dynamic1 and dynamic2 do not affect this value.

Operator sizeof is especially useful to get the sizes of [classes](/en/book/oop/classes_and_interfaces) and [structures](/en/book/oop/structs_and_unions).

typename

Operator typename returns a string with the name of the parameter passed to it, which can be a type or an expression. For arrays, along with the data type keyword, a tag is printed as a pair of parentheses (or several ones, depending on the array dimensionality).

```
Print(typename(double));                         // double
Print(typename(array));                          // double [2][2]
Print(typename(dynamic1));                       // double [][1]
Print(typename(1 + 2));                          // int

```

For custom types, such as classes, structures, and others (that we will consider in Part 3), the type name follows the entity category, such as "class MyCustomType". Moreover, for constants, the "const" modifier will be added to the string description.

Therefore, to know the short type name consisting of one word, use macro TYPENAME from the attached file TypeName.mqh.

It can be necessary to learn the type name in the so-called [templates](/en/book/oop/templates) that can generate from the source code similar realizations for different types defined in the parameters of templates.
