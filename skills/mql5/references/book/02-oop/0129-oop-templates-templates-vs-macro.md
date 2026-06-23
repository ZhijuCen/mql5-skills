# Templates vs preprocessor macros

A question may arise at some point, is it possible to use macro substitutions for the purposes of code generation? It is actually possible. For example, the set of Max functions can be easily represented as a macro:

```
#define MAX(V1,V2) ((V1) > (V2) ? (V1) : (V2))

```

However, macros have more limited capabilities (nothing more than text substitution) and therefore they are only used in simple cases (like the one above).

When comparing macros and templates, the following differences should be noted.

Macros are "expanded" and replaced in the source text by the preprocessor before compilation starts. At the same time, there is no information about the types of parameters and the context in which the contents of the macro are substituted. In particular, the macro MAX cannot provide a check-up that the types of the parameters V1 and V2 are the same, and also that the comparison operator '>' is defined for them. In addition, if a variable with the name MAX is encountered in a program text, the preprocessor will try to substitute the "call" of the MAX macro in its place and will be "unhappy" with the absence of arguments. Worse yet, these substitutions ignore which namespaces or classes the MAX token is found in – basically, any will do.

Unlike macros, templates are handled by the compiler in terms of specific argument types and where they are used, so they provide type compatibility (and general applicability) checks for all expressions in a template, as well as context binding. For example, we can define a method template within a concrete class.

A template with the same name can be defined differently for different types if necessary, while a macro with a given name is always replaced by the same "implementation". For example, in the case of a function like MAX, we could define a case-insensitive comparison for strings.

Compilation errors due to problems in macros are difficult to diagnose, especially if the macro consists of several lines, since the problematic line with the "call" of the macro is highlighted "as is", without the expanded version of the text, as it came from the preprocessor to the compiler.

At the same time, templates are elements of the source code in a ready-made form, as they enter the compiler, and therefore any error in them has a specific line number and position in the line.

Macros can have side effects, which we discussed in the [Form of #define as a pseudo-function](/en/book/basis/preprocessor/preprocessor_define_functional) section: if the MAX macro arguments are expressions with increments/decrements, then they will be executed twice.

However, macros also have some advantages. Macros are capable of generating any text, not just correct language constructs. For example, with a few macros, you can simulate the instruction switch for strings (although this approach is not recommended).

In the standard library, macros are used, in particular, to organize the processing of events on charts (see MQL5/Include/Controls/Defines.mqh: EVENT_MAP_BEGIN, EVENT_MAP_END, ON_EVENT, etc.). It will not work on templates, but the way of arranging an event map on macros, of course, is far from the only one and not the most convenient for debugging. It is difficult to debug step-by-step (line-by-line) code execution in macros. Templates, on the contrary, support debugging in full.
