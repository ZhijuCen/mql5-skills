# Type conversion

In this section, we will consider the concept of type conversion, limiting ourselves to built-in data types for now. Later, after studying OOP, we will supplement it with the nuances inherent in object types.

Type conversion in MQL5 is the process of changing the data type of a variable or expression. MQL5 supports three main types of type conversion: implicit, arithmetic, and explicit.

[Implicit type conversion](/en/book/basis/conversion/conversion_implicit):

- Occurs automatically when a variable of one type is used in a context that expects another type. For example, integer values can be implicitly converted to real values.

[Arithmetic type conversion](/en/book/basis/conversion/conversion_arithmetic):

- Arises during arithmetic operations with operands of different types. The compiler attempts to maintain maximum accuracy but warns about potential data loss. For instance, in integer division, the result is converted to a real type.

[Explicit type conversion](/en/book/basis/conversion/conversion_explicit):

- Gives the programmer control over type conversion. It is done in two forms: C-style ((target)) and "functional" style (target()). It is used when you need to explicitly instruct the compiler to perform a conversion between types, for example, when rounding real numbers or when successive type conversions are required.

Understanding the differences between implicit, arithmetic, and explicit type conversion is crucial for ensuring the correct execution of operations and avoiding data loss. This knowledge helps programmers effectively utilize this mechanism in MQL5 development.
