# Templates

In modern programming languages, there are many built-in features that allow you to avoid code duplication and, thereby, minimize the number of errors and increase programmer productivity. In MQL5, such tools include the already known [functions](/en/book/basis/functions), object types with inheritance support ([classes](/en/book/oop/classes_and_interfaces) and [structures](/en/book/oop/structs_and_unions)), [preprocessor macros](/en/book/basis/preprocessor/preprocessor_define_functional), and the ability to [include files](/en/book/basis/preprocessor/preprocessor_include). But this list would be incomplete without templates.

A template is a specially crafted generic definition of a function or object type from which the compiler can automatically generate working instances of that function or object type. The resulting instances contain the same algorithm but operate on variables of different types, corresponding to the specific conditions for using the template in the source code.

For C++ connoisseurs, we note that MQL5 templates do not support many features of C++ templates, in particular:

- parameters that are not types;
- parameters with default values;
- variable number of parameters;
- specialization of classes, structures, and associations (full and partial);
- templates for templates.

On the one hand, this reduces the potential of templates in MQL5, but, on the other hand, it simplifies the learning of the material for those who are unfamiliar with these technologies.
