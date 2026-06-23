# Void Type and NULL Constant

Syntactically the void type is a fundamental type along with types of char, uchar, bool, short, ushort, int, uint, color, long, ulong, datetime, float, double and string. This type is used either to indicate that the function does not return any value, or as a function parameter it denotes the absence of parameters.

The predefined constant variable NULL is of the void type. It can be assigned to variables of any other fundamental types without conversion. The comparison of fundamental type variables with the NULL value is allowed.

Example:

```
//--- If the string is not initialized, then assign our predefined value to it
if(some_string==NULL) some_string="empty";

```

Also NULL can be compared to pointers to objects created with the [new operator](/en/docs/basis/operators/newoperator).

See also

[Variables](/en/docs/basis/variables), [Functions](/en/docs/basis/function)
