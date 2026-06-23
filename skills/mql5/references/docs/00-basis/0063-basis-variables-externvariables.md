# Extern Variables

The extern keyword is used for declaring variable identifiers as identifiers of the [static storage class](/en/docs/basis/variables/static) with global [lifetime](/en/docs/basis/variables/variable_scope). These variables exist from the start of the program and memory for them is allocated and initialized immediately after the start of the program.

You can create programs that consist of multiple source files; in this case a directive to the preprocessor [#include](/en/docs/basis/preprosessor/include) is used. Variables declared as an extern with the same type and identifier can exist in different source files of one project.

When compiling the whole project, all the extern variables with the same type and an identifier are associated with one part of memory of the global variable pool. Extern variables are useful for separate compilation of source files. Extern variables can be initialized, but only once - existence of several initialized extern variables of the same type and with the same identifier is prohibited.

See also

[Data Types](/en/docs/basis/types), [Encapsulation and Extensibility of Types](/en/docs/basis/oop/incapsulation),[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live)
